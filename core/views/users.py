from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.forms import PasswordResetForm
from ..forms.users import (
    UserRegistrationForm,UserLoginForm,PasswordResetForm,
    UserPasswordChangeForm,UserProfileForm, CustomUserFullProfileForm
)
from urllib.parse import urlparse

from .. models import CustomUser

from django.contrib.auth.decorators import user_passes_test

# method for redirecting users
def redirect_authenticated_user(user):
    return not user.is_authenticated  # Prevent access if user is logged in

def home(request):
    return render(request, 'base/home.html')

def dashboard(request):
    return render(request, 'base/dashboard.html')


## user sign in / registration view
@user_passes_test(redirect_authenticated_user, login_url='/')
def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("core:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    
    return render(request, "core/users/register.html", {"form": form})


## user login
@user_passes_test(redirect_authenticated_user, login_url='/')
def login_user(request):
    next_url = request.GET.get("next", "core:home")  # Get 'next' parameter or default to home

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")

                # Ensure next_url is safe (prevents open redirect vulnerability)
                if urlparse(next_url).netloc == "":
                    return redirect(next_url)
                return redirect("core:home")  # Fallback to home if next_url is unsafe
            else:
                messages.error(request, "Invalid credentials, please try again.")
    else:
        form = UserLoginForm()

    return render(request, "core/users/login.html", {"form": form, "next": next_url})


## Logout function
@login_required
def logout_user(request):
    logout(request)
    request.session.flush()
    # messages.success(request, "You have been logged out.")
    return redirect("core:login")

# logout function
def logout_inactive_user(request):
    logout(request)
    request.session.flush()
    return render(request, 'core/users/inactive_user.html')


## reset forgotten password without sending an email
def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            new_password = form.cleaned_data["new_password"]
            user = get_object_or_404(CustomUser, email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful! You can now log in.")
            return redirect("core:login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordResetForm()

    return render(request, "core/users/password_reset.html", {"form": form})


## change passworg (for users who remember password and are logged in)
@login_required
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            messages.success(request, "Password updated successfully!")
            return redirect("core:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserPasswordChangeForm(request.user)

    return render(request, "core/users/password_change.html", {"form": form})


## View user profile
@login_required
def profile_view(request):
    return render(request, "core/users/profile.html", {"user": request.user})


# update user profile
@login_required
def profile_update(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("core:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=user)

    return render(request, "core/users/profile_edit.html", {"form": form})


#list all users
@login_required
def user_list(request):
    users = CustomUser.objects.all()  # Fetch all users
    return render(request, 'core/users/user_list.html', {'users': users})


@login_required
def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    user.is_active = False
    user.save()
    messages.success(request, f"{user.get_full_name()} has been deactivated.")
    return redirect(request.META.get('HTTP_REFERER', 'core:user_list'))

@login_required
def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    user.is_active = True
    user.save()
    messages.success(request, f"{user.get_full_name()} has been activated.")
    return redirect(request.META.get('HTTP_REFERER', 'core:user_list'))

@login_required
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'core/users/user_detail.html', {'u': user})


## function called by high level users
@login_required
def edit_user_profile(request, user_id):
    u = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = CustomUserFullProfileForm(request.POST, instance=u)
        if form.is_valid():
            form.save()
            messages.success(request, "User details updated successfully.")
            return redirect('core:user_detail', user_id=u.id)  # Redirect to user detail page
    else:
        form = CustomUserFullProfileForm(instance=u)

    return render(request, 'core/users/edit_full_profile.html', {'form': form, 'user': u})
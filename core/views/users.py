from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.forms import PasswordResetForm
from ..forms.users import UserRegistrationForm,UserLoginForm,PasswordResetForm,UserPasswordChangeForm,UserProfileForm
from .. models import CustomUser

from django.contrib.auth.decorators import user_passes_test

# method for redirecting users
def redirect_authenticated_user(user):
    return not user.is_authenticated  # Prevent access if user is logged in

def home(request):
    return render(request, 'base/home.html')


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
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("core:home")
            else:
                messages.error(request, "Invalid credentials, please try again.")
    else:
        form = UserLoginForm()
    
    return render(request, "core/users/login.html", {"form": form})


## Logout function
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("core:login")


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

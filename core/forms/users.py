from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from ..models import CustomUser
from django.core.exceptions import ValidationError

User = get_user_model()


### user registration form
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={"class": "form-control border-info", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={"class": "form-control border-info", "placeholder": "Last Name"})
    )
    payroll = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={"class": "form-control border-info", "placeholder": "Payroll Number"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control border-info", "placeholder": "Email"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control border-info", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control border-info", "placeholder": "Confirm Password"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "payroll", "password1", "password2"]

    def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this email already exists.")
            return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone

    def clean_payroll(self):
        payroll = self.cleaned_data.get('payroll')
        if payroll and User.objects.filter(payroll=payroll).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this payroll number already exists.")
        return payroll

    def clean_medical_cert_number(self):
        medical_cert_number = self.cleaned_data.get('medical_cert_number')
        if medical_cert_number and User.objects.filter(medical_cert_number=medical_cert_number).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this medical certificate number already exists.")
        return medical_cert_number

## user login form
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )

## forgot password reset form
class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New Password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


## Change password for users who remember their password
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Old Password"})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New Password"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm New Password"})
    )

## update user profile / update my profile

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "readonly": "readonly"})
    )
    phone = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]

    def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this email already exists.")
            return email

    def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this phone number already exists.")
            return phone


class CustomUserFullProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'payroll', 'role',
            'medical_cert_number', 'medical_cert_generation_date', 'medical_cert_expiry_date',
            'department', 'job', 'is_active', 'is_staff'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'payroll': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter payroll number'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'medical_cert_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter medical cert number'}),
            'medical_cert_generation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'medical_cert_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'job': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this email already exists.")
            return email

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this phone number already exists.")
            return phone

        def clean_payroll(self):
            payroll = self.cleaned_data.get('payroll')
            if payroll and User.objects.filter(payroll=payroll).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this payroll number already exists.")
            return payroll

        def clean_medical_cert_number(self):
            medical_cert_number = self.cleaned_data.get('medical_cert_number')
            if medical_cert_number and User.objects.filter(medical_cert_number=medical_cert_number).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this medical certificate number already exists.")
            return medical_cert_number

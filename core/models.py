from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                   on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name="%(class)s_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                   on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name="%(class)s_updated")

    class Meta:
        abstract = True


class Department(BaseModel):
    department = models.CharField(max_length=50, unique=True)
    description=models.TextField(null=True, blank=True)
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_department'
    )

    def __str__(self):
        return self.department.department()


class Plant(BaseModel):
    plant = models.CharField(max_length=50, unique=True)
    description=models.TextField(blank=True, null=True)

    def __str__(self):
        return self.plant.plant()


class Job(BaseModel):
    job = models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.job.job()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('supervisor', 'Supervisor'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    payroll = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='supervisor')
    medical_cert_number = models.CharField(max_length=100, blank=True, null=True)
    medical_cert_generation_date = models.DateField(blank=True, null=True)
    medical_cert_expiry_date = models.DateField(blank=True, null=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name='User'
        verbose_name_plural="Users"

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}" if self.first_name and self.last_name else self.email
    
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}" if self.first_name and self.last_name else self.email
    
    def assignments(self):
        """Returns active assignments for the current date"""
        today = now().date()
        return self.assignments.filter(start_date__lte=today, end_date__gte=today)  # Filtering active assignments


class Casual(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    payroll = models.CharField(max_length=20, blank=True, null=True, unique=True)
    medical_cert_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    medical_cert_generation_date = models.DateField(blank=True, null=True)
    medical_cert_expiry_date = models.DateField(blank=True, null=True)
    valid_cert = models.BooleanField(default=False)  # New field

    class Meta:
        ordering=['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"
    
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def check_certificate_validity(self):
        """Checks if 6 months have elapsed since medical_cert_generation_date."""
        if self.medical_cert_generation_date:
            six_months_later = self.medical_cert_generation_date + timedelta(days=180)
            return now().date() <= six_months_later
        return False

    def save(self, *args, **kwargs):
        """Automatically updates valid_cert before saving."""
        self.valid_cert = self.check_certificate_validity()
        super().save(*args, **kwargs)

    def has_medical_cert(self):
        return self.valid_cert
    
    def has_payroll(self):
        return self.payroll_number is not None
    
    def has_payment(self):
        return self.phone is not None
    
class UserAssignment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignments")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="assignments")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.plant.plant} ({self.start_date} to {self.end_date if self.end_date else 'Ongoing'})"


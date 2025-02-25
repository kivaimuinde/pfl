from django.contrib import admin
from django.utils.timezone import now
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from .models import Department, Plant, Role, CustomUser, Casual, UserAssignment


class AutoUserMixin:
    """Mixin to auto-fill created_by and updated_by fields."""
    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by:
            obj.created_by = request.user  # Set created_by on creation
        obj.updated_by = request.user  # Always update updated_by
        super().save_model(request, obj, form, change)


class BaseAdmin(AutoUserMixin, admin.ModelAdmin):
    """Base admin with common fields."""
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    list_display = ("created_at", "updated_at", "created_by", "updated_by")
    list_filter = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(Department)
class DepartmentAdmin(BaseAdmin):
    list_display = ("department", "description") + BaseAdmin.list_display
    search_fields = ("department", )


@admin.register(Plant)
class PlantAdmin(BaseAdmin):
    list_display = ("plant", "description") + BaseAdmin.list_display
    search_fields = ("plant", )


@admin.register(Role)
class RoleAdmin(BaseAdmin):
    list_display = ("role", "description") + BaseAdmin.list_display
    search_fields = ("role", "description")


class CustomUserForm(ModelForm):
    """Ensures password fields are not required when editing users."""
    class Meta:
        model = CustomUser
        fields = '__all__'


@admin.register(CustomUser)
class CustomUserAdmin(AutoUserMixin, UserAdmin):
    ordering = ("email",)  # Set ordering to use 'email' instead of 'username'
    list_display = ("email", "first_name", "last_name", "department", "role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name", "department__department", "role__role")
    readonly_fields = ("last_login", "created_at", "updated_at", "created_by", "updated_by")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone", "payroll_number")}),
        ("Employment", {"fields": ("department", "role")}),
        ("Medical Info", {"fields": ("medical_cert_number", "medical_cert_generation_date", "medical_cert_expiry_date")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "created_at", "updated_at", "created_by", "updated_by")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )


@admin.register(Casual)
class CasualAdmin(BaseAdmin):
    list_display = ("first_name", "last_name", "phone", "payroll_number", "valid_cert") + BaseAdmin.list_display
    search_fields = ("first_name", "last_name", "phone", "payroll_number", "medical_cert_number")
    list_filter = ("valid_cert",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "phone", "payroll_number")}),
        ("Medical Info", {"fields": ("medical_cert_number", "medical_cert_generation_date", "medical_cert_expiry_date", "valid_cert")}),
        ("Metadata", {"fields": ("created_at", "updated_at", "created_by", "updated_by")}),
    )


@admin.register(UserAssignment)
class UserAssignmentAdmin(BaseAdmin):
    list_display = ("user", "plant", "start_date", "end_date") + BaseAdmin.list_display
    search_fields = ("user__email", "user__first_name", "user__last_name", "plant__plant")
    list_filter = ("start_date", "end_date")

    def active_assignments(self, obj):
        """Show active assignments only."""
        return obj.start_date <= now().date() and (obj.end_date is None or obj.end_date >= now().date())
    active_assignments.boolean = True  # Show as a Boolean icon in the admin

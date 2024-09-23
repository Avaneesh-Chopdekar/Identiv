from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import LoginLog, Person


# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin panel
    list_display = ("email", "first_name", "last_name", "is_staff")

    # Define the fields to use when adding a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    # Define the fields for the user form in the admin panel
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Tell Django to use the email field as the unique identifier
    search_fields = ("email",)
    ordering = ("email",)


# Register the Organization model with the customized admin class
admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Person)
admin.site.register(LoginLog)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Organization,
    Person,
    PersonDetail,
    LoginLog,
    Role,
    CustomField,
    Feedback,
    Option,
)


# Register your models here.
class OrganizationAdmin(UserAdmin):
    # Define the fields to display in the admin panel
    list_display = ("email", "organization_name", "is_staff")

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
        (None, {"fields": ("organization_name", "email", "password")}),
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
    search_fields = ("email", "organization_name")
    ordering = ("email",)


# Register the Organization model with the customized admin class
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(LoginLog)
admin.site.register(PersonDetail)
admin.site.register(CustomField)
admin.site.register(Option)
admin.site.register(Feedback)

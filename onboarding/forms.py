from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    SetPasswordForm,
    PasswordResetForm,
)
from django.utils.translation import gettext_lazy as _
from app.models import Organization


class OrganizationCreationForm(UserCreationForm):
    class Meta:
        model = Organization
        fields = [
            "email",
            "organization_name",
            "phone_number",
            "address",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].widget.attrs.update(
            {
                "placeholder": "Enter phone number starting with country code e.g. +91 9876543210"
            }
        )
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class OrganizationLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "placeholder": "Enter your email",
                "autofocus": True,
            }
        ),
        error_messages={
            "required": _("Please enter your email address."),
            "invalid": _("Enter a valid email address."),
        },
    )

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "input mb-2", "placeholder": "Enter your password"}
        ),
        error_messages={"required": _("Please enter your password.")},
    )


class EditOrganizationDetailsForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["email", "organization_name", "phone_number", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

    # Optional: Add custom validation if needed
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            Organization.objects.filter(email=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Email address is already in use.")
        return email


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "placeholder": "Enter your email",
            }
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Enter new password",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Confirm new password",
            }
        )
    )

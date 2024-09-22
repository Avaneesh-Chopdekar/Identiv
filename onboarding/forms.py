# myapp/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class OrganizationCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"required": "required"})
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

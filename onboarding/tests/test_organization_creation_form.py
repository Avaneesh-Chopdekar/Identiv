from django.test import TestCase
from onboarding.forms import OrganizationCreationForm


class OrganizationCreationFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            "email": "test@example.com",
            "organization_name": "Test Organization",
            "phone_number": "+911234567890",
            "address": "123 Test Street",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
        }
        form = OrganizationCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_mismatch(self):
        form_data = {
            "email": "test@example.com",
            "organization_name": "Test Organization",
            "phone_number": "+911234567890",
            "address": "123 Test Street",
            "password1": "complexpassword123",
            "password2": "differentpassword",
        }
        form = OrganizationCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_missing_email(self):
        form_data = {
            "organization_name": "Test Organization",
            "phone_number": "+911234567890",
            "address": "123 Test Street",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
        }
        form = OrganizationCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

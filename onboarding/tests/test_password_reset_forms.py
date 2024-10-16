from django.test import TestCase
from app.models import Organization
from onboarding.forms import CustomPasswordResetForm, CustomSetPasswordForm


class CustomPasswordResetFormTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            organization_name="Test Organization",
            email="test@example.com",
            password="testpass123",
        )

    def test_form_valid(self):
        form_data = {
            "email": "test@example.com",
        }
        form = CustomPasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_email(self):
        form_data = {
            "email": "",
        }
        form = CustomPasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class CustomSetPasswordFormTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            organization_name="Test Organization",
            email="test@example.com",
            password="testpass123",
        )

    def test_form_valid(self):
        form_data = {
            "email": "test@example.com",
            "new_password1": "newstrongpassword123",
            "new_password2": "newstrongpassword123",
        }
        form = CustomSetPasswordForm(user=self.organization, data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_mismatch(self):
        form_data = {
            "new_password1": "newstrongpassword123",
            "new_password2": "differentpassword",
        }
        form = CustomSetPasswordForm(user=self.organization, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("new_password2", form.errors)

    def test_form_invalid_missing_password(self):
        form_data = {
            "new_password1": "",
            "new_password2": "",
        }
        form = CustomSetPasswordForm(user=self.organization, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("new_password1", form.errors)

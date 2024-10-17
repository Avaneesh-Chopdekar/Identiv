from django.test import TestCase
from app.models import Organization
from onboarding.forms import OrganizationLoginForm


class OrganizationLoginFormTest(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            organization_name="Test Organization",
            email="logintest@example.com",
        )
        self.organization.set_password("testpass123")
        self.organization.save()

    def test_form_valid(self):
        form_data = {
            "username": "logintest@example.com",
            "password": "testpass123",
        }
        form = OrganizationLoginForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_invalid_no_email(self):
        form_data = {
            "username": "",
            "password": "testpass123",
        }
        form = OrganizationLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_invalid_no_password(self):
        form_data = {
            "username": "logintest@example.com",
            "password": "",
        }
        form = OrganizationLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

from django.test import TestCase
from django.forms import ValidationError
from app.models import Organization
from dashboard.forms import CustomFieldForm, OptionForm
from dashboard.models import CustomField, Option


class FormTestCase(TestCase):
    def setUp(self):
        # Set up test data for organization and custom fields
        self.organization = Organization.objects.create(
            organization_name="Test Organization",
            email="org@example.com",
            password="testpass123",
        )

        self.custom_field_data = {
            "name": "Role",
            "field_type": "Radio",
        }

        self.option_data = {
            "option_name": "Guest",
        }

    def test_custom_field_form_valid(self):
        # Test a valid CustomFieldForm
        form = CustomFieldForm(data=self.custom_field_data)
        self.assertTrue(form.is_valid())
        custom_field = form.save(commit=False)
        custom_field.organization = self.organization
        custom_field.save()
        self.assertEqual(custom_field.name, "Role")
        self.assertEqual(custom_field.field_type, "Radio")

    def test_custom_field_form_invalid(self):
        # Test an invalid CustomFieldForm (missing name)
        invalid_data = {"name": "", "field_type": "Radio"}
        form = CustomFieldForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)  # Check that name field has errors

    def test_option_form_valid(self):
        # Test a valid OptionForm
        custom_field = CustomField.objects.create(
            organization=self.organization, name="Role", field_type="Radio"
        )
        form = OptionForm(data=self.option_data)
        self.assertTrue(form.is_valid())
        option = form.save(commit=False)
        option.custom_field = custom_field
        option.save()
        self.assertEqual(option.option_name, "Guest")

    def test_option_form_invalid(self):
        # Test an invalid OptionForm (missing option_name)
        invalid_data = {"option_name": ""}
        form = OptionForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "option_name", form.errors
        )  # Check that option_name field has errors

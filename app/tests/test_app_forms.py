from django.test import TestCase
from app.forms import RegistrationForm
from app.models import Person, Organization
from dashboard.models import CustomField, Option


class RegistrationFormTest(TestCase):
    def setUp(self):
        # Create an organization
        self.organization = Organization.objects.create(
            organization_name="Test Org",
            email="org@example.com",
            password="testpass123",
        )

        self.face_embedding = [0.12 for _ in range(128)]

        # Create custom fields for the organization
        self.role_field = CustomField.objects.create(
            name="Role", field_type="Radio", organization=self.organization
        )
        self.interests_field = CustomField.objects.create(
            name="Interests", field_type="Checkbox", organization=self.organization
        )

        # Create options for custom fields
        self.role_option1 = Option.objects.create(
            custom_field=self.role_field, option_name="Developer"
        )
        self.role_option2 = Option.objects.create(
            custom_field=self.role_field, option_name="Designer"
        )

        self.interests_option1 = Option.objects.create(
            custom_field=self.interests_field, option_name="Music"
        )
        self.interests_option2 = Option.objects.create(
            custom_field=self.interests_field, option_name="Sports"
        )

        # Test data for person
        self.person_data = {
            "first_name": "John",
            "middle_name": "M",
            "last_name": "Doe",
            "Role": str(self.role_option1.id),  # Pass the ID as a string for Radio
            "Interests": [
                str(self.interests_option1.id),
                str(self.interests_option2.id),
            ],  # List of strings for Checkbox
        }

    def test_registration_form_valid(self):
        # Test form is valid with correct data
        form = RegistrationForm(data=self.person_data, organization=self.organization)
        self.assertTrue(form.is_valid())  # This should pass now

        # Continue with saving the form data if valid
        person = form.save(commit=False)
        person.face_embedding = self.face_embedding
        person.organization = self.organization
        person.save()
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.middle_name, "M")
        self.assertEqual(person.last_name, "Doe")

    def test_registration_form_checkbox_selection(self):
        # Test with multiple selected options for checkbox field
        form = RegistrationForm(data=self.person_data, organization=self.organization)
        self.assertTrue(form.is_valid())  # Should pass now for checkbox selection

from django.test import TestCase
from app.models import Organization


class OrganizationModelTest(TestCase):
    def test_create_user(self):
        """Test creating a user"""
        organization_name = "Organization Test"
        email = "test@example.com"
        phone_number = "+91 1112223330"
        address = "123 Main St"
        password = "cjld2cjxh0000qzrmn831i7rn"

        user = Organization.objects.create(
            organization_name=organization_name,
            email=email,
            phone_number=phone_number,
            address=address,
        )
        user.set_password(password)

        self.assertEqual(user.organization_name, organization_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.address, address)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        organization_name = "Super Organization Test"
        email = "super.test@example.com"
        phone_number = "+91 1112224440"
        address = "124 Main St"
        password = "cjld2cjxh0000qzrmn831i7rn"

        user = Organization.objects.create_superuser(
            organization_name=organization_name,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password,
        )

        self.assertEqual(user.organization_name, organization_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.address, address)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

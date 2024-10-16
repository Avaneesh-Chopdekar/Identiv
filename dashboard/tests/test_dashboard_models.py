from django.test import TestCase
from app.models import Person, Organization
from dashboard.models import (
    LoginLog,
    CustomField,
    Option,
    PersonDetail,
    Notification,
    Blacklist,
)
from django.utils import timezone


class DashboardModelsTestCase(TestCase):

    def setUp(self):
        # Setup test data here
        self.organization = Organization.objects.create(
            organization_name="Test Organization",
            email="org@example.com",
            password="testpass123",
        )

        self.person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            middle_name="M",
            face_embedding=[0.1 for _ in range(128)],
        )

        self.login_time = timezone.now()

    def test_login_log_creation(self):
        # Create LoginLog
        login_log = LoginLog.objects.create(
            person=self.person,
            organization=self.organization,
            login_time=self.login_time,
        )
        self.assertEqual(
            str(login_log),
            f"{self.login_time.strftime('%Y-%m-%d %H:%M:%S')} by John Doe from Test Organization",
        )

    def test_custom_field_creation(self):
        # Create a CustomField
        custom_field = CustomField.objects.create(
            organization=self.organization, name="Role", field_type="Radio"
        )
        self.assertEqual(str(custom_field), "Role (Radio) for Test Organization")

    def test_option_creation(self):
        # Create a CustomField and Option
        custom_field = CustomField.objects.create(
            organization=self.organization, name="Role", field_type="Radio"
        )
        option = Option.objects.create(custom_field=custom_field, option_name="Guest")
        self.assertEqual(str(option), "Option: Guest | Field: Role")

    def test_person_detail_creation(self):
        # Create a CustomField, Option, and PersonDetail
        custom_field = CustomField.objects.create(
            organization=self.organization, name="Role", field_type="Radio"
        )
        person_detail = PersonDetail.objects.create(
            person=self.person,
            custom_field=custom_field,
        )
        self.assertEqual(
            str(person_detail), f"Response of John Doe to Role from Test Organization"
        )

    def test_notification_creation(self):
        # Create a Notification
        notification = Notification.objects.create(
            person=self.person,
            organization=self.organization,
            status=Notification.PENDING,
        )
        self.assertEqual(
            str(notification),
            f"Notification for {self.organization} from {self.person}",
        )

    def test_blacklist_creation(self):
        # Create a Blacklist entry
        blacklist = Blacklist.objects.create(
            person=self.person,
            organization=self.organization,
            reason="Violation of rules",
        )
        self.assertEqual(
            str(blacklist), f"Blacklisted {self.person} from {self.organization}"
        )
        self.assertEqual(blacklist.reason, "Violation of rules")

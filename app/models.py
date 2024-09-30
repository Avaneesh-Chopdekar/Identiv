from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from pgvector.django import VectorField

from app.manager import OrganizationManager


class Organization(AbstractUser):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)  # Make email the unique identifier
    organization_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    roles = models.ManyToManyField("Role", related_name="organizations")

    username = None  # Remove username field

    USERNAME_FIELD = "email"  # Replace username with email
    REQUIRED_FIELDS = ["organization_name"]  # Required fields other than email

    objects = OrganizationManager()

    def __str__(self):
        return f"{self.organization_name} | {self.email}"


class Role(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="defined_roles"
    )

    def __str__(self):
        return f"{self.name} on {self.organization.organization_name}"


class Person(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizations = models.ManyToManyField(Organization, related_name="people")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    face_embedding = VectorField(dimensions=128)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    class Meta:
        indexes = [
            models.Index(fields=["face_embedding"]),
            models.Index(fields=["first_name", "last_name"]),
        ]


class LoginLog(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.login_time.strftime('%Y-%m-%d %H:%M:%S')} by {self.person.first_name} {self.person.last_name} from {self.organization.organization_name}"

    class Meta:
        unique_together = (
            "person",
            "organization",
            "login_time",
        )  # Ensure unique person and time entry


class CustomField(models.Model):
    FIELD_TYPES = (
        ("Text", "Text"),
        ("BigText", "BigText"),
        ("Radio", "Radio"),
        ("Checkbox", "Checkbox"),
    )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="custom_fields"
    )
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES, default="Text")

    def __str__(self):
        return (
            f"{self.name} ({self.field_type}) for {self.organization.organization_name}"
        )


class Option(models.Model):
    custom_field = models.ForeignKey(
        CustomField, on_delete=models.CASCADE, related_name="options"
    )
    option_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Option: {self.option_name} | Field: {self.custom_field.name}"


class PersonDetails(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="person_details"
    )
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    response_text = models.TextField(
        null=True, blank=True
    )  # For Text and BigText responses
    selected_options = models.ManyToManyField(Option, blank=True)  # For Radio/Checkbox

    class Meta:
        unique_together = [
            "person",
            "custom_field",
        ]  # Ensure one person has one record per organization

    def __str__(self):
        return f"Response of {self.person.first_name} {self.person.last_name} to {self.custom_field.name} from {self.custom_field.organization.organization_name}"


class Feedback(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="feedbacks"
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="feedbacks"
    )
    custom_fields = models.ManyToManyField(CustomField)

    def __str__(self):
        return f"Feedback from {self.person.first_name} {self.person.last_name} for {self.organization.organization_name}"

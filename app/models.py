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

    username = None  # Remove username field

    USERNAME_FIELD = "email"  # Replace username with email
    REQUIRED_FIELDS = ["organization_name"]  # Required fields other than email

    objects = OrganizationManager()

    def __str__(self):
        return f"{self.organization_name} | {self.email}"


class Person(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizations = models.ManyToManyField(Organization, related_name="people")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    face_embedding = VectorField(dimensions=128)
    is_active = models.BooleanField(
        default=False
    )  # To prevent login if registration not accepted
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

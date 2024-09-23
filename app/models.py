from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
import uuid

from app.manager import OrganizationManager


class Organization(AbstractUser):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)  # Make email the unique identifier
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    username = None  # Remove username field

    USERNAME_FIELD = "email"  # Replace username with email
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Required fields other than email

    objects = OrganizationManager()

    def __str__(self):
        return f"{self.name} | {self.email}"


User = get_user_model()


class Person(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    face_embedding = ArrayField(models.FloatField(), size=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.organization.name}"


class LoginLog(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.login_time} | {self.person.name} | {self.person.organization.name}"
        )

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Group(AbstractUser):
    email = models.EmailField(unique=True)  # Make email the unique identifier
    group_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"  # Replace username with email
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Required fields other than email

    def __str__(self):
        return f"{self.group_name} | {self.email}"


class Person(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    face_embedding = ArrayField(models.FloatField(), size=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.group.group_name}"


class LoginLog(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.login_time} | {self.person.name} | {self.person.group.group_name}"
        )

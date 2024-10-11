import uuid
from django.db import models
from app.models import Person, Organization


# Create your models here.
class LoginLog(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="login_logs"
    )
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


class PersonDetail(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="person_detail"
    )
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    response_text = models.TextField(
        null=True, blank=True
    )  # For Text and BigText responses
    selected_options = models.ManyToManyField(Option, blank=True)  # For Radio/Checkbox

    class Meta:
        unique_together = ("person", "custom_field")

    def __str__(self):
        return f"Response of {self.person.first_name} {self.person.last_name} to {self.custom_field.name} from {self.custom_field.organization.organization_name}"


class Notification(models.Model):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    ]

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.organization} from {self.person}"


class Blacklist(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    blacklisted_on = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Blacklisted People"

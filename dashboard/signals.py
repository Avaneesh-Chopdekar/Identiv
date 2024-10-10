from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Person, Notification, Organization


@receiver(m2m_changed, sender=Person.organizations.through)
def create_notification(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    This signal is triggered when a person is added to a new organization.
    It sends a notification to the new organization for approval.
    """
    if action == "post_add":
        # `instance` refers to the Person instance
        # `pk_set` refers to the set of new organization IDs the person was added to
        for org_pk in pk_set:
            organization = Organization.objects.get(pk=org_pk)

            # Check if a notification for this organization and person already exists
            if not Notification.objects.filter(
                person=instance, organization=organization
            ).exists():
                Notification.objects.create(
                    person=instance,
                    organization=organization,
                )

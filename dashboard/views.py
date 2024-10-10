from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from app.models import Person
from dashboard.forms import CustomFieldForm, OptionForm
from dashboard.models import Blacklist, CustomField, Notification, Option, PersonDetail


# Create your views here.
@login_required
def registration_fields(request):
    """
    Handle form submission for creating custom fields and adding options to them.
    """
    # Initialize the forms
    custom_field_form = CustomFieldForm()
    option_form = OptionForm()
    edit_field_instance = None  # To track the field being edited

    if request.method == "POST":
        # Handle form submission for creating a new custom field
        if "create_field" in request.POST:
            custom_field_form = CustomFieldForm(request.POST)
            if custom_field_form.is_valid():
                custom_field = custom_field_form.save(commit=False)
                custom_field.organization = (
                    request.user
                )  # Assign the current organization
                custom_field.save()
                return redirect("registration_fields")  # Redirect to the same view

        # Handle form submission for adding options to a custom field
        elif "add_option" in request.POST:
            field_id = request.POST.get(
                "field_id"
            )  # Get the field ID from a hidden input
            custom_field = get_object_or_404(
                CustomField, uid=field_id, organization=request.user
            )
            option_form = OptionForm(request.POST)
            if option_form.is_valid():
                option = option_form.save(commit=False)
                option.custom_field = (
                    custom_field  # Link the option to the custom field
                )
                option.save()
                return redirect("registration_fields")  # Redirect to the same view

        # Handle deleting a custom field
        elif "delete_field" in request.POST:
            field = get_object_or_404(CustomField, uid=request.POST["field_id"])
            field.delete()
            return redirect("registration_fields")

        # Handle deleting an option
        elif "delete_option" in request.POST:
            option = get_object_or_404(Option, id=request.POST["option_id"])
            option.delete()
            return redirect("registration_fields")

        # Handle editing a custom field
        elif "edit_field" in request.POST:
            field = get_object_or_404(CustomField, uid=request.POST["field_id"])
            custom_field_form = CustomFieldForm(request.POST, instance=field)
            if custom_field_form.is_valid():
                custom_field_form.save()
                return redirect("registration_fields")

    # Fetch custom fields created by the logged-in organization
    custom_fields = CustomField.objects.filter(organization=request.user)
    custom_field_form = CustomFieldForm(instance=edit_field_instance)

    context = {
        "custom_field_form": custom_field_form,
        "option_form": option_form,
        "custom_fields": custom_fields,
        "edit_field_instance": edit_field_instance,  # Pass the field being edited
    }

    # Render the page with the forms and custom fields
    return render(
        request,
        "dashboard/registration_fields.html",  # Make sure the template path matches your folder structure
        context,
    )


@login_required
def people_view(request):
    search_query = request.GET.get("search", "")
    filters = {}

    # Iterate over GET parameters to capture selected filters
    for key, value in request.GET.items():
        if key != "search" and value:
            filters[key] = value

    # Get current organization
    organization = request.user

    # Fetch people from the same organization and apply search filter
    people = organization.people.filter(
        Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
    ).prefetch_related("person_detail__custom_field", "person_detail__selected_options")

    # Apply custom field filters
    for field_name, option_value in filters.items():
        people = people.filter(
            person_detail__custom_field__name=field_name,
            person_detail__selected_options__option_name=option_value,
        )

    # Create a dictionary to store person details efficiently
    people_details = PersonDetail.objects.filter(
        person__in=people, custom_field__organization=organization
    )

    context = {
        "people": people,
        "people_details": people_details,
        "custom_fields": organization.custom_fields.filter(
            field_type__in=["Radio", "Checkbox"]
        ),
    }
    return render(request, "dashboard/people.html", context)


@login_required
def logs_view(request):
    search_query = request.GET.get("search", "").strip()
    organization = (
        request.user
    )  # Assuming the logged-in user belongs to one organization

    # Access people related to the current organization through the Many-to-Many relationship
    if search_query:
        # Filter people based on first name or last name and ensure they belong to the current organization
        logs = organization.login_logs.filter(
            Q(person__first_name__icontains=search_query)
            | Q(person__last_name__icontains=search_query)
        ).order_by("-login_time")
    else:
        # If no search query, show all people from the current organization
        logs = organization.login_logs.all().order_by("-login_time")

    context = {"logs": logs, "search_query": search_query}
    return render(request, "dashboard/logs.html", context)


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(organization=request.user)

    if request.method == "POST":
        notification_id = request.POST["notification_id"]
        decision = request.POST["decision"]
        notification = get_object_or_404(Notification, uid=notification_id)

        if decision == "approve":
            # Add the person to the organization and approve their membership in this specific org
            notification.organization.people.add(notification.person)
            notification.person.is_active = True  # Mark as approved for this org
            notification.person.save()
        elif decision == "reject":
            # If rejected, remove from the organization and add to blacklist
            notification.organization.people.remove(notification.person)
            Blacklist.objects.create(
                person=notification.person, organization=notification.organization
            )

        notification.delete()  # Remove the notification after action is taken
        return redirect("notifications")  # Reload the page

    return render(
        request, "dashboard/notifications.html", {"notifications": notifications}
    )


@login_required
def delete_person(request, person_id):
    try:
        person = Person.objects.get(pk=person_id)
        person.delete()
        messages.success(request, "Person deleted successfully.")
    except Person.DoesNotExist:
        messages.error(request, "Person not found.")
    return redirect("people")


@login_required
def blacklist(request):
    search_query = request.GET.get("search", "").strip()

    if search_query:
        # Filter people based on first name or last name and ensure they belong to the current organization
        blacklist = Blacklist.objects.filter(
            Q(person__first_name__icontains=search_query)
            | Q(person__last_name__icontains=search_query),
            organization=request.user,
        ).order_by("-blacklisted_on")
    else:
        # If no search query, show all people from the current organization
        blacklist = Blacklist.objects.all().order_by("-blacklisted_on")

    context = {"blacklist": blacklist, "search_query": search_query}
    return render(request, "dashboard/blacklist.html", context)

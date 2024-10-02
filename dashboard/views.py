from django.shortcuts import get_object_or_404, redirect, render

from dashboard.forms import CustomFieldForm, OptionForm
from dashboard.models import CustomField, Option


# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")


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
    if request.method == "POST" and "delete_field" in request.POST:
        field = get_object_or_404(CustomField, uid=request.POST["field_id"])
        field.delete()
        return redirect("registration_fields")

    # Handle deleting an option
    if request.method == "POST" and "delete_option" in request.POST:
        option = get_object_or_404(Option, id=request.POST["option_id"])
        option.delete()
        return redirect("registration_fields")

    # Handle editing a custom field
    if request.method == "POST" and "edit_field" in request.POST:
        field = get_object_or_404(CustomField, uid=request.POST["field_id"])
        custom_field_form = CustomFieldForm(request.POST, instance=field)
        if custom_field_form.is_valid():
            custom_field_form.save()
            return redirect("registration_fields")

    # Fetch custom fields created by the logged-in organization
    custom_fields = CustomField.objects.filter(organization=request.user)
    custom_field_form = CustomFieldForm(instance=edit_field_instance)
    # Render the page with the forms and custom fields
    return render(
        request,
        "dashboard/registration_fields.html",  # Make sure the template path matches your folder structure
        {
            "custom_field_form": custom_field_form,
            "option_form": option_form,
            "custom_fields": custom_fields,
            "edit_field_instance": edit_field_instance,  # Pass the field being edited
        },
    )


def people(request):
    return render(request, "dashboard/people.html")


def logs(request):
    return render(request, "dashboard/logs.html")


def notifications(request):
    return render(request, "dashboard/notifications.html")

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from datetime import datetime
from face_recognition import face_encodings
from app.models import Person
from app.forms import RegistrationForm
from dashboard.models import CustomField, LoginLog, PersonDetail
from antispoofing.test import test
from .utils import (
    find_person_by_embedding,
    extract_image_from_data_uri,
    has_already_sent_registration_request,
    is_blacklisted,
)


@login_required
@require_POST
@ensure_csrf_cookie
def face_login(request):
    label = test(
        image_path=request.POST.get("image_data"),
        model_dir="./antispoofing/resources/anti_spoof_models",
        device_id=0,
    )

    if label == 1:
        image = extract_image_from_data_uri(request.POST.get("image_data"))

        if image is None:
            return JsonResponse(
                {"status": "error", "message": "Invalid image data!"}, status=400
            )

        face_embedding = face_encodings(image)[0]

        if face_embedding is None:
            return JsonResponse(
                {"status": "error", "message": "No face detected!"}, status=400
            )

        # Now, search for the person by embedding
        person = find_person_by_embedding(face_embedding, request.user)

        if is_blacklisted(face_embedding, request.user):
            return JsonResponse(
                {"status": "error", "message": "You are blacklisted!"}, status=401
            )

        if has_already_sent_registration_request(face_embedding, request.user):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "You cannot login until your registration is accepted by the organization.",
                },
                status=400,
            )

        if person:
            organization = request.user  # Assuming the current organization context

            if not person.organizations.filter(pk=organization.pk).exists():
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "You are not a member of this organization",
                    }
                )

            # Log the login attempt
            LoginLog.objects.create(
                person=person, login_time=datetime.now, organization=request.user
            )
            return JsonResponse(
                {"status": "success", "message": "Logged in successfully!"}
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "User not registered!"}, status=401
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Spoofing detected!"}, status=401
        )


# Create your views here.
@login_required
def index(request):
    return render(
        request, "app/index.html", {"organization_name": request.user.organization_name}
    )


@login_required
def register(request):
    if request.method == "POST":
        organization = request.user
        form = RegistrationForm(request.POST, organization=request.user)
        image_data = request.POST.get("image_data")

        if form.is_valid():
            label = test(
                image_path=image_data,
                model_dir="./antispoofing/resources/anti_spoof_models",
                device_id=0,
            )

            if label != 1:
                return JsonResponse(
                    {"status": "error", "message": "Spoofing detected!"}, status=401
                )

            image = extract_image_from_data_uri(image_data)

            if image is None:
                return JsonResponse(
                    {"status": "error", "message": "Invalid image data!"}, status=400
                )

            face_embedding = face_encodings(image)[0]

            if face_embedding is None:
                return JsonResponse(
                    {"status": "error", "message": "No face detected!"}, status=400
                )

            person = find_person_by_embedding(face_embedding)

            if is_blacklisted(face_embedding, request.user):
                return JsonResponse(
                    {"status": "error", "message": "You are blacklisted!"}, status=401
                )

            if has_already_sent_registration_request(face_embedding, request.user):
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "You have already sent a registration request to this organization.",
                    },
                    status=400,
                )

            if person is None:
                person = form.save(commit=False)
                person.face_embedding = face_embedding
                person.save()

            person.organizations.add(organization)

            # Save custom field responses
            for custom_field in CustomField.objects.filter(organization=request.user):
                response_value = form.cleaned_data.get(custom_field.name)
                if custom_field.field_type in ["Text", "BigText"]:
                    PersonDetail.objects.create(
                        person=person,
                        custom_field=custom_field,
                        response_text=response_value,
                    )
                else:
                    # For Radio/Checkbox fields
                    selected_options = form.cleaned_data.get(custom_field.name)
                    person_detail = PersonDetail.objects.create(
                        person=person, custom_field=custom_field
                    )
                    person_detail.selected_options.set(selected_options)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "You can login after organization approves your registration request!",
                }
            )

    else:
        form = RegistrationForm(organization=request.user)

    return render(
        request, "app/register.html", {"form": form, "organization": request.user}
    )

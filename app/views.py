from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from datetime import datetime
from face_recognition import face_encodings
import posthog
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
            posthog.capture(
                request.user.uid,  # The unique identifier of the user (can be the user's ID or email)
                "login:app:no_image",  # The event name
                {"organization_name": request.user.organization_name},
            )
            return JsonResponse(
                {"status": "error", "message": "Invalid image data!"}, status=400
            )

        face_embedding = face_encodings(image)[0]

        if face_embedding is None:
            posthog.capture(
                request.user.uid,  # The unique identifier of the user (can be the user's ID or email)
                "login:app:no_face_detected",  # The event name
                {"organization_name": request.user.organization_name},
            )
            return JsonResponse(
                {"status": "error", "message": "No face detected!"}, status=400
            )

        # Now, search for the person by embedding
        person = find_person_by_embedding(face_embedding, request.user)

        if is_blacklisted(face_embedding, request.user):
            posthog.capture(
                person.uid,  # The unique identifier of the user (can be the user's ID or email)
                "login:person:blacklisted_detection",  # The event name
                {
                    "first_name": person.first_name,
                    "middle_name": person.middle_name,
                    "last_name": person.last_name,
                    "organization_name": request.user.organization_name,
                },
            )
            return JsonResponse(
                {"status": "error", "message": "You are blacklisted!"}, status=401
            )

        if has_already_sent_registration_request(face_embedding, request.user):
            posthog.capture(
                person.uid,  # The unique identifier of the user (can be the user's ID or email)
                "login:person:registration_request_not_approved",  # The event name
                {
                    "first_name": person.first_name,
                    "middle_name": person.middle_name,
                    "last_name": person.last_name,
                    "organization_name": request.user.organization_name,
                },
            )
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
                posthog.capture(
                    person.uid,  # The unique identifier of the user (can be the user's ID or email)
                    "login:person:not_a_member",  # The event name
                    {
                        "first_name": person.first_name,
                        "middle_name": person.middle_name,
                        "last_name": person.last_name,
                        "organization_name": organization.organization_name,
                    },
                )
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
            posthog.capture(
                person.uid,  # The unique identifier of the user (can be the user's ID or email)
                "login:person:success",  # The event name
                {
                    "first_name": person.first_name,
                    "middle_name": person.middle_name,
                    "last_name": person.last_name,
                    "organization_name": request.user.organization_name,
                },
            )
            return JsonResponse(
                {"status": "success", "message": "Logged in successfully!"}
            )
        else:
            posthog.capture(
                request.user.uid,  # The unique identifier of the user (can be the user's ID or email)
                "login:person:not_registered",  # The event name
                {
                    "organization_name": request.user.organization_name,
                },
            )
            return JsonResponse(
                {"status": "error", "message": "User not registered!"}, status=401
            )
    else:
        posthog.capture(
            request.user.uid,  # The unique identifier of the user (can be the user's ID or email)
            "login:person:spoofing_detection",  # The event name
            {
                "organization_name": request.user.organization_name,
            },
        )
        return JsonResponse(
            {"status": "error", "message": "Spoofing detected!"}, status=401
        )


# Create your views here.
@login_required
def index(request):
    posthog.capture(request.user.uid, "$pageview")
    return render(
        request, "app/index.html", {"organization_name": request.user.organization_name}
    )


@login_required
def register(request):
    posthog.capture(request.user.uid, "$pageview")
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
                posthog.capture(
                    request.user.uid,  # The unique identifier of the user (can be the user's ID or email)
                    "register:organization:spoofing_detected",  # The event name
                    {
                        "organization_name": request.user.organization_name,
                    },
                )
                return JsonResponse(
                    {"status": "error", "message": "Spoofing detected!"}, status=401
                )

            image = extract_image_from_data_uri(image_data)

            if image is None:
                posthog.capture(
                    request.user.uid,  # The unique identifier of the user (can be the user's ID or email)
                    "register:organization:no_image",  # The event name
                    {
                        "organization_name": request.user.organization_name,
                    },
                )
                return JsonResponse(
                    {"status": "error", "message": "Invalid image data!"}, status=400
                )

            face_embedding = face_encodings(image)[0]

            if face_embedding is None:
                posthog.capture(
                    request.user.uid,  # The unique identifier of the user (can be the user's ID or email)
                    "login:person:no_face_detected",  # The event name
                    {
                        "organization_name": request.user.organization_name,
                    },
                )
                return JsonResponse(
                    {"status": "error", "message": "No face detected!"}, status=400
                )

            person = find_person_by_embedding(face_embedding)

            if is_blacklisted(face_embedding, request.user):
                posthog.capture(
                    person.uid,  # The unique identifier of the user (can be the user's ID or email)
                    "register:person:blacklisted_detection",  # The event name
                    {
                        "first_name": person.first_name,
                        "middle_name": person.middle_name,
                        "last_name": person.last_name,
                        "organization_name": request.user.organization_name,
                    },
                )
                return JsonResponse(
                    {"status": "error", "message": "You are blacklisted!"}, status=401
                )

            if has_already_sent_registration_request(face_embedding, request.user):
                posthog.capture(
                    person.uid,  # The unique identifier of the user (can be the user's ID or email)
                    "register:person:registration_request_not_approved",  # The event name
                    {
                        "first_name": person.first_name,
                        "middle_name": person.middle_name,
                        "last_name": person.last_name,
                        "organization_name": request.user.organization_name,
                    },
                )
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
                posthog.capture(
                    person.uid,  # The unique identifier of the user (can be the user's ID or email)
                    "register:person:new_person_created",  # The event name
                    {
                        "first_name": person.first_name,
                        "middle_name": person.middle_name,
                        "last_name": person.last_name,
                        "organization_name": request.user.organization_name,
                    },
                )

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

            posthog.capture(
                person.uid,  # The unique identifier of the user (can be the user's ID or email)
                "register:person:success",  # The event name
                {
                    "first_name": person.first_name,
                    "middle_name": person.middle_name,
                    "last_name": person.last_name,
                    "organization_name": request.user.organization_name,
                },
            )
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

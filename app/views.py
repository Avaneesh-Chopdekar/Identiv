import base64
import cv2
import numpy as np
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.shortcuts import render
from face_recognition import face_encodings, compare_faces, load_image_file
from dashboard.models import LoginLog
from datetime import datetime
from antispoofing.test import test
from .utils import find_person_by_embedding, extract_image_from_data_uri


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

        # Now, search for the person by embedding
        person = find_person_by_embedding(face_embedding)

        if person:
            # Log the login attempt
            LoginLog.objects.create(person=person, login_time=datetime.now)
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
    return render(request, "app/register.html")

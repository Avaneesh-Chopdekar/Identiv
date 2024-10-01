from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registration_fields/", views.registration_fields, name="registration_fields"),
    path("people/", views.people, name="people"),
    path("logs/", views.logs, name="logs"),
    path("notifications/", views.notifications, name="notifications"),
]

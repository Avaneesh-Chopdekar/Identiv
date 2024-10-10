from django.urls import path
from . import views

urlpatterns = [
    path("registration-fields/", views.registration_fields, name="registration_fields"),
    path("people/", views.people_view, name="people"),
    path("logs/", views.logs_view, name="logs"),
    path("blacklist/", views.blacklist, name="blacklist"),
    path("notifications/", views.notifications_view, name="notifications"),
    path("delete-person/<person_id>/", views.delete_person, name="delete_person"),
]

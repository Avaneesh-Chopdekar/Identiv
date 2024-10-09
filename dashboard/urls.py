from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path("registration_fields/", views.registration_fields, name="registration_fields"),
    path("people/", views.people_view, name="people"),
    path("logs/", views.logs_view, name="logs"),
    path("notifications/", views.notifications_view, name="notifications"),
    path("delete_person/<person_id>/", views.delete_person, name="delete_person"),
]

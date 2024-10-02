from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="app_index"),
    path("face-login/", views.face_login, name="face_login"),
    path("register/", views.register, name="register"),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("how-to-use/", views.how_to_use, name="how_to_use"),
    path("purpose/", views.purpose, name="purpose"),
    # Auth routes
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.account, name="account"),
    path("account/edit/", views.edit_account, name="edit_account"),
    path("account/delete/", views.delete_account, name="delete_account"),
    # Password reset routes
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

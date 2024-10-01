from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_views

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
        "reset_password/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="onboarding/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="onboarding/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Dashboard Routes
    path("dashboard/", dashboard_views.index, name="dashboard"),
]

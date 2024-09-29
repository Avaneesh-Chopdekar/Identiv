from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms

User = get_user_model()


# Create your views here.
def landing_page(request):
    faqs = [
        {
            "question": "What is Identiv and how does it work?",
            "answer": "Identiv is a cutting-edge identity verification app that uses face recognition and anti-spoofing technology to authenticate users quickly and securely.",
        },
        {
            "question": "Is my data secure?",
            "answer": "Yes, your data is fully encrypted and handled with the utmost security measures, ensuring that your personal information is safe.",
        },
        {
            "question": "How fast is the verification process?",
            "answer": "The verification process takes only a few seconds, providing a seamless experience without compromising security.",
        },
        {
            "question": "What devices are supported?",
            "answer": "Identiv is compatible with most devices that have a front camera, including smartphones, tablets, and computers.",
        },
    ]
    return render(request, "onboarding/index.html", context={"faqs": faqs})


def how_to_use(request):
    return render(request, "onboarding/how_to_use.html")


def purpose(request):
    return render(request, "onboarding/purpose.html")


def signup_view(request):
    if request.method == "POST":
        form = forms.OrganizationCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = forms.OrganizationCreationForm()
    return render(request, "onboarding/signup.html", {"form": form})


class CustomLoginView(LoginView):
    form_class = forms.OrganizationLoginForm
    template_name = "onboarding/login.html"


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    return render(request, "onboarding/logout.html")


@login_required
def delete_account(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        logout(request)
        return redirect("signup")
    return render(request, "onboarding/delete_account.html")


@login_required
def account(request):
    return render(request, "onboarding/account.html")


@login_required
def edit_account(request):
    user = request.user
    if request.method == "POST":
        form = forms.EditOrganizationDetailsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("account")
    else:
        form = forms.EditOrganizationDetailsForm(instance=user)

    return render(request, "onboarding/edit_account.html", {"form": form})


class CustomPasswordResetView(PasswordResetView):
    form_class = forms.CustomPasswordResetForm
    template_name = "onboarding/password_reset.html"

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "There is no user registered with this email address."
            )
        return email


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = forms.CustomSetPasswordForm
    template_name = "onboarding/password_reset_confirm.html"

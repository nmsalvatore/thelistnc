from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from accounts.forms import LoginForm

from decouple import config
import random
import time

@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Handle user login
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "GET":
        form = LoginForm()
        context = {"form": form}
        return render(request, "accounts/login.html", context)

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            recipient_email = form.cleaned_data["email"]

            try:
                user = User.objects.get(email=recipient_email)
                otp = str(random.randint(100000, 999999))

                request.session["email"] = recipient_email
                request.session["otp"] = otp
                request.session["otp_timestamp"] = time.time()
                request.session["attempt_count"] = 0

                from_email = config("EMAIL_USER")

                send_mail(
                    "The List NC Verification Code",
                    f"Your one-time passcode is: {otp}",
                    f"The List NC <{from_email}>",
                    [recipient_email],
                    fail_silently=False,
                )

                return redirect("verify_login_otp")

            except User.DoesNotExist:
                form.add_error("email", "No account is associated with this email address.")
                context = {"form": form}
                return render(request, "accounts/login.html", context)


@require_http_methods(["GET", "POST"])
def verify_login_otp(request):
    """
    Complete user login with one-time passcode
    """
    email = request.session.get("email")
    otp_timestamp = request.session.get("otp_timestamp")
    time_elapsed = time.time() - otp_timestamp
    stored_otp = request.session.get("otp")
    attempt_count = request.session.get("attempt_count")
    verify_template = "accounts/verify_otp.html"

    if request.method == "GET":
        context = {"email": email}
        return render(request, verify_template, context)

    if request.method == "POST":
        attempt_count += 1
        request.session["attempt_count"] = attempt_count
        context = {"email": email}

        if time_elapsed > 300:
            context["error_message"] = "Passcode has expired. Navigate back to login page to start over."
            return render(request, verify_template, context)

        if attempt_count > 3:
            context["error_message"] = "Attempt limit has been reached. Navigate back to login page to start over."
            return render(request, verify_template, context)

        otp = request.POST.get("otp")
        if not otp:
            context["error_message"] = "Please enter a valid passcode."
            return render(request, verify_template, context)

        stored_otp = request.session.get("otp")
        if not stored_otp:
            context["error_message"] = "Something went wrong."
            return render(request, verify_template, context)

        if otp!= stored_otp and attempt_count == 3:
            context["error_message"] = "Invalid passcode. Attempt limit has been reached."
            return render(request, verify_template, context)

        if otp != stored_otp:
            context["error_message"] = "Invalid passcode."
            return render(request, verify_template, context)

        user = User.objects.get(email=email)
        login(request, user)
        delete_session_data(request)
        return redirect("dashboard")


def delete_session_data(request):
    del request.session["email"]
    del request.session["otp"]
    del request.session["otp_timestamp"]
    del request.session["attempt_count"]

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods, require_GET
from decouple import config

from accounts.models import Invitation, UserProfile
from accounts.forms import RegistrationForm
from accounts.decorators import invitation_required

import random
import time


@require_http_methods(["GET", "POST"])
@invitation_required
def register_view(request):
    """
    Handle user registration via invite
    """
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            recipient_email = form.cleaned_data["email"]
            invitation = request.invitation

            if invitation.email != recipient_email:
                form.add_error("email", "Invalid email for the given invitation code.")
                return render(request, "accounts/register.html", {"form": form})

            otp = str(random.randint(100000, 999999))
            request.session["email"] = recipient_email
            request.session["otp"] = otp
            request.session["otp_timestamp"] = time.time()
            request.session["invitation_id"] = invitation.id
            request.session["attempt_count"] = 0

            from_email = config('EMAIL_USER')

            send_mail(
                "The List NC Verification Code",
                f"Your one-time passcode is: {otp}",
                f"The List NC <{from_email}>",
                [recipient_email],
                fail_silently=False,
            )

            return redirect("verify_register_otp")


@require_http_methods(["GET", "POST"])
def verify_register_otp(request):
    """
    Complete registration with one-time passcode
    """
    email = request.session.get("email")
    otp_timestamp = request.session.get("otp_timestamp")
    time_elapsed = time.time() - otp_timestamp
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
            context["error_message"] = "Passcode has expired. Follow the link in the invitation email to start over."
            return render(request, verify_template, context)

        if attempt_count > 3:
            context["error_message"] = "Attempt limit has been reached. Follow the link in the invitation email to start over."
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

        user = create_user(email)
        use_invitation(request)
        delete_session_data(request)
        login(request, user)
        return redirect("registration_success")


@require_GET
def registration_success(request):
    if request.user.is_authenticated:
        return render(request, "accounts/registration_success.html")
    else:
        return redirect("home")


def delete_session_data(request):
    del request.session["email"]
    del request.session["otp"]
    del request.session["otp_timestamp"]
    del request.session["invitation_id"]
    del request.session["attempt_count"]


def create_user(email):
    user = User.objects.create_user(username=email, email=email)
    UserProfile.objects.create(user=user)
    return user


def use_invitation(request):
    invitation_id = request.session.get("invitation_id")
    invitation = Invitation.objects.get(id=invitation_id)
    invitation.is_used = True
    invitation.save()

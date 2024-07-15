from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from decouple import config

from accounts.models import Invitation, UserProfile
from accounts.forms import RegistrationForm
from accounts.decorators import invitation_required

import random
import time


@invitation_required
def register_view(request):
    """
    Handle user registration via invite
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            invitation = request.invitation

            if invitation.email != email:
                form.add_error("email", "Invalid email for the given invitation code.")
                return render(request, "accounts/register.html", {"form": form})

            otp = str(random.randint(100000, 999999))
            request.session["email"] = email
            request.session["otp"] = otp
            request.session["otp_timestamp"] = time.time()
            request.session["invitation_id"] = invitation.id
            request.session["attempt_count"] = 0

            send_mail(
                "Your one-time passcode",
                f"Your one-time passcode is: {otp}",
                config('EMAIL_USER'),
                [email],
                fail_silently=False,
            )

            return redirect("verify_register_otp")

    form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


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
            error_message = "Passcode has expired."
            context["error_message"] = error_message
            return render(request, verify_template, context)

        if attempt_count == 3:
            error_message = "Invalid passcode. Attempt limit has been reached."
            context["error_message"] = error_message
            return render(request, verify_template, context)

        if attempt_count > 3:
            error_message = "Attempt limit has been exceeded."
            context["error_message"] = error_message
            return render(request, verify_template, context)

        otp = request.POST.get("otp")
        if not otp:
            error_message = "Please enter a valid passcode"
            context["error_message"] = error_message
            return render(request, verify_template, context)

        stored_otp = request.session.get("otp")
        if not stored_otp:
            error_message = "Something went wrong."
            context["error_message"] = error_message
            return render(request, verify_template, context)

        if otp != stored_otp:
            error_message = "Invalid passcode."
            context["error_message"] = error_message
            return render(request, verify_template, context)

        user = create_user(email)
        use_invitation(request)
        delete_session_data(request)
        login(request, user)
        return redirect("registration_success")

    return redirect("home")


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

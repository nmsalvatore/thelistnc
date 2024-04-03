from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail

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
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            invitation = request.invitation

            if invitation.email == email:
                otp = str(random.randint(100000, 999999))
                request.session['email'] = email
                request.session['otp'] = otp
                request.session['otp_timestamp'] = time.time()
                request.session['invitation_id'] = invitation.id

                # Send OTP via email
                send_mail(
                    'Your one-time passcode',
                    f'Your one-time passcode is: {otp}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )

                return redirect('verify_register_otp')
            else:
                form.add_error('email', 'Invalid email for the given invitation code.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def verify_register_otp(request):
    """
    Complete registration with one-time passcode
    """
    email = request.session.get('email')
    otp_timestamp = request.session.get('otp_timestamp')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        invitation_id = request.session.get('invitation_id')

        if otp and stored_otp and otp == stored_otp:
            if time.time() - otp_timestamp <= 300:
                user = User.objects.create_user(username=email, email=email)
                UserProfile.objects.create(user=user)

                invitation = Invitation.objects.get(id=invitation_id)
                invitation.is_used = True
                invitation.save()

                del request.session['email']
                del request.session['otp']
                del request.session['otp_timestamp']
                del request.session['invitation_id']

                login(request, user)
                return redirect('registration_success')
            else:
                error_message = 'Passcode has expired.'
                context = {
                    'email': email,
                    'error_message': error_message,
                    'otp_timestamp': otp_timestamp
                }
                return render(request, 'verify_otp.html', context)
        else:
            error_message = 'Invalid passcode.'
            context = {
                'email': email,
                'error_message': error_message,
                'otp_timestamp': otp_timestamp,
            }
            return render(request, 'verify_otp.html', context)
    else:
        context = {
            'email': email,
            'otp_timestamp': otp_timestamp,
        }
        return render(request, 'verify_otp.html', {'email': email})


def registration_success(request):
    return render(request, 'registration_success.html')

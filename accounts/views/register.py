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

                # Initialize session data
                request.session['email'] = email
                request.session['otp'] = otp
                request.session['otp_timestamp'] = time.time()
                request.session['invitation_id'] = invitation.id
                request.session['attempt_count'] = 0

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

    # Retrieve session data
    email = request.session.get('email')
    stored_otp = request.session.get('otp')
    otp_timestamp = request.session.get('otp_timestamp')
    attempt_count = request.session.get('attempt_count')

    # GET request logic
    if request.method == 'GET':
        context = {
            'email': email,
        }
        return render(request, 'verify_otp.html', {'email': email})

    # POST request logic
    if request.method == 'POST':

        # Increment attempt count and save to session
        attempt_count += 1
        request.session['attempt_count'] = attempt_count

        # Retrieve form OTP value
        otp = request.POST.get('otp')

        # Retrieve invitation ID
        invitation_id = request.session.get('invitation_id')

        # If attempts exceed 3, throw error
        if attempt_count > 3:
            error_message = 'Attempt limit has been exceeded.'
            context = {
                'email': email,
                'error_message': error_message,
            }
            return render(request, 'verify_otp.html', context)

        # Check for matching OTP values
        if otp and stored_otp and otp == stored_otp:

            # If OTP values match and 5 minutes has not passed, create and log in user
            if time.time() - otp_timestamp <= 300:

                # Add user to database
                user = User.objects.create_user(username=email, email=email)
                UserProfile.objects.create(user=user)

                # Mark user invitation as used
                invitation = Invitation.objects.get(id=invitation_id)
                invitation.is_used = True
                invitation.save()

                # Delete session data
                del request.session['email']
                del request.session['otp']
                del request.session['otp_timestamp']
                del request.session['invitation_id']
                del request.session['attempt_count']

                # Log in user
                login(request, user)

                return redirect('registration_success')
            
            # If stored OTP has expired, throw error
            else:
                error_message = 'Passcode has expired.'
                context = {
                    'email': email,
                    'error_message': error_message,
                }
                return render(request, 'verify_otp.html', context)
        
        # If OTP values do not match, throw error
        else:
            error_message = 'Invalid passcode.'
            context = {
                'email': email,
                'error_message': error_message,
            }
            return render(request, 'verify_otp.html', context)
        
    # If request is not POST or GET, redirect to home
    else:
        return redirect('home')


def registration_success(request):
    return render(request, 'registration_success.html')

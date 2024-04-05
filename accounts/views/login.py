from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from accounts.forms import LoginForm

import random
import time


def login_view(request):
    """
    Handle user login
    """
    if request.user.is_authenticated:
        return redirect(reverse('dashboard', args=['by-date']))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))

                # Initialize session data
                request.session['email'] = email
                request.session['otp'] = otp
                request.session['otp_timestamp'] = time.time()
                request.session['attempt_count'] = 0

                # Send OTP via email
                send_mail(
                    'Your one-time passcode',
                    f'Your one-time passcode is: {otp}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )

                return redirect('verify_login_otp')
            except User.DoesNotExist:
                form.add_error('email', 'No account is associated with this email address.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def verify_login_otp(request):
    """
    Complete user login with one-time passcode
    """

    # Retrieve session data
    email = request.session.get('email')
    otp_timestamp = request.session.get('otp_timestamp')
    stored_otp = request.session.get('otp')
    attempt_count = request.session.get('attempt_count')

    # GET request logic
    if request.method == 'GET':
        context = {
            'email': email,
        }
        return render(request, 'verify_otp.html', context)

    # POST request logic
    if request.method == 'POST':

        # Increment attempt count and save to session
        attempt_count += 1
        request.session['attempt_count'] = attempt_count

        # Retrieve form OTP value
        otp = request.POST.get('otp')

        # If attempts exceed 3, throw error
        if attempt_count > 3:
            error_message = 'Attempt limit has been exceeded.'
            context = {
                'email': email,
                'error_message': error_message
            }
            return render(request, 'verify_otp.html', context)

        # Check for matching OTP values
        if otp and stored_otp and otp == stored_otp:

            # If OTP values match and stored OTP has not expired, log in user
            if time.time() - otp_timestamp <= 300:

                # Log in user
                user = User.objects.get(email=email)
                login(request, user)

                # Clear session data
                del request.session['email']
                del request.session['otp']
                del request.session['otp_timestamp']
                del request.session['attempt_count']

                return redirect(reverse('dashboard', args=['by-date']))

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

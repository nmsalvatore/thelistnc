from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from accounts.forms import LoginForm

import random
import time


def login_view(request):
    """
    Handle user login
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                request.session['email'] = email
                request.session['otp'] = otp
                request.session['otp_timestamp'] = time.time()

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
    email = request.session.get('email')
    otp_timestamp = request.session.get('otp_timestamp')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if otp and stored_otp and otp == stored_otp:
            if time.time() - otp_timestamp <= 300:
                user = User.objects.get(email=email)
                login(request, user)

                del request.session['email']
                del request.session['otp']
                del request.session['otp_timestamp']

                return redirect('dashboard')
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
                'otp_timestamp': otp_timestamp
            }
            return render(request, 'verify_otp.html', context)
    else:
        context = {
            'email': email,
            'otp_timestamp': otp_timestamp
        }
        return render(request, 'verify_otp.html', context)

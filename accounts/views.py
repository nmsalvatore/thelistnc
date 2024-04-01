from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Invitation, UserProfile
from .forms import RegistrationForm, LoginForm
from .decorators import invitation_required

import random


@invitation_required
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            invitation = request.invitation

            if invitation.email == email:
                # Generate OTP
                otp = str(random.randint(100000, 999999))
                request.session['email'] = email
                request.session['otp'] = otp
                request.session['invitation_id'] = invitation.id

                # Send OTP via email
                send_mail(
                    'Registration OTP',
                    f'Your OTP is: {otp}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )

                return redirect('verify_otp')
            else:
                form.add_error('email', 'Invalid email for the given invitation code.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        stored_otp = request.session.get('otp')
        invitation_id = request.session.get('invitation_id')

        if otp == stored_otp:
            # Create user account
            user = User.objects.create_user(username=email, email=email)
            UserProfile.objects.create(user=user)

            # Mark invitation as used
            invitation = Invitation.objects.get(id=invitation_id)
            invitation.is_used = True
            invitation.save()

            # Clear session data
            del request.session['email']
            del request.session['otp']
            del request.session['invitation_id']

            # Login user
            login(request, user)

            return redirect('home')
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'verify_otp.html', {'error_message': error_message})
    else:
        return render(request, 'verify_otp.html')
    

def registration_success(request):
    return render(request, 'registration_success.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate OTP
                otp = str(random.randint(100000, 999999))
                request.session['email'] = email
                request.session['otp'] = otp

                # Send OTP via email
                send_mail(
                    'Login OTP',
                    f'Your OTP is: {otp}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )

                return redirect('verify_login_otp')
            except User.DoesNotExist:
                form.add_error('email', 'Email does not exist. Please register first.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def verify_login_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        stored_otp = request.session.get('otp')

        if otp == stored_otp:
            user = User.objects.get(email=email)
            login(request, user)

            del request.session['email']
            del request.session['otp']

            return redirect('home')
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'verify_otp.html', {'error_message': error_message})
    else:
        return render(request, 'verify_otp.html')


def logout_view(request):
    logout(request)
    return redirect('home')

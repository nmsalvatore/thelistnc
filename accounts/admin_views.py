from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config

from .models import Invitation


@user_passes_test(lambda u: u.is_superuser)
def send_invitation(request):
    if request.method == 'POST':
        email = request.POST['email']
        invitation = Invitation.objects.create(email=email)

        # Send email with invitation code using Mailgun SMTP
        subject = 'You\'ve been invited to be a moderator for The List NC'
        registration_url = f'http://localhost:8000/moderator/register?code={invitation.code}'
        context = {
            'email': email,
            'registration_url': registration_url,
        }
        html_message = render_to_string('invitation_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = config('VERIFIED_SENDER')
        recipient_list = [email]

        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

        return redirect('invitation_sent')

    return render(request, 'send_invitation.html')


@user_passes_test(lambda u: u.is_superuser)
def invitation_sent(request):
    return render(request, 'invitation_sent.html')

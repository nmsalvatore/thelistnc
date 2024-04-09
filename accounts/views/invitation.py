from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config

from accounts.models import Invitation


@user_passes_test(lambda u: u.is_superuser)
def send_invitation(request):
    if request.method == 'POST':
        # Get email from form
        email = request.POST['email']

        # Check for previous invitations
        already_invited = Invitation.objects.filter(email=email)
        if already_invited:
            error_message = 'User has already received an invitation.'
            return render(request, 'send_invitation.html', {'error_message': error_message})

        # Create invitation
        invitation = Invitation.objects.create(email=email)

        # Configure email for Mailgun SMTP
        subject = 'You\'ve been invited to be a moderator for The List NC'
        base_url = config('BASE_URL')
        registration_url = f'{base_url}/admin/register?code={invitation.code}'
        context = {
            'email': email,
            'registration_url': registration_url,
        }
        html_message = render_to_string('invitation_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = config('EMAIL_INVITE_SENDER')
        recipient_list = [email]

        # Send email using Mailgun SMTP
        try:
            send_mail(
                subject,
                plain_message,
                from_email,
                recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
        except:
            error_message = 'User email has not been verified with Mailgun.'
            invitation.delete()
            return render(request, 'send_invitation.html', {'error_message': error_message})

        return redirect('invitation_sent')

    return render(request, 'send_invitation.html')


@user_passes_test(lambda u: u.is_superuser)
def invitation_sent(request):
    return render(request, 'invitation_sent.html')

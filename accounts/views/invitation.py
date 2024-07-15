from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_http_methods, require_GET

from decouple import config

from accounts.models import Invitation


@require_http_methods(["GET", "POST"])
@user_passes_test(lambda u: u.is_superuser)
def send_invitation(request):
    if request.method == "GET":
        return render(request, 'accounts/send_invitation.html')

    if request.method == 'POST':
        email = request.POST['email']

        already_invited = Invitation.objects.filter(email=email)
        if already_invited:
            error_message = 'User has already received an invitation.'
            return render(request, 'accounts/send_invitation.html', {'error_message': error_message})

        invitation = Invitation.objects.create(email=email)
        try:
            send_invitation_email(email, invitation)
        except:
            error_message = 'Something went wrong.'
            invitation.delete()
            return render(request, 'accounts/send_invitation.html', {'error_message': error_message})

        return redirect('invitation_sent')


@require_GET
@user_passes_test(lambda u: u.is_superuser)
def invitation_sent(request):
    return render(request, 'accounts/invitation_sent.html')


def send_invitation_email(recipient_email, invitation):
    subject = 'You\'ve been invited to be a volunteer for The List NC'
    base_url = config('BASE_URL')
    registration_url = f'{base_url}/accounts/register?code={invitation.code}'
    context = {
        'email': recipient_email,
        'registration_url': registration_url,
    }
    html_message = render_to_string('accounts/invitation_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = config('EMAIL_USER')
    recipient_list = [recipient_email]

    send_mail(
        subject,
        plain_message,
        f"The List NC <{from_email}>",
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

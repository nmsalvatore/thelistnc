from django.shortcuts import redirect
from django.urls import reverse


def admin(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard', args=['by-date']))

    else:
        return redirect('login')
from django.shortcuts import redirect
from .models import Invitation


def invitation_required(view_func):
    def wrapper(request, *args, **kwargs):
        code = request.GET.get('code')
        try:
            invitation = Invitation.objects.get(code=code, is_used=False)
            request.invitation = invitation
            return view_func(request, *args, **kwargs)
        except (Invitation.DoesNotExist, ValueError):
            return redirect('invitation_required')
    return wrapper

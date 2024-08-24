from django.shortcuts import redirect


def admin_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

from django.shortcuts import render, redirect


def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/dashboard.html')
    else:
        return redirect('login')

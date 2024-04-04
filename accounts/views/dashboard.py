from django.shortcuts import render, redirect


def dashboard_view(request):
    if request.user.is_superuser:
        return render(request, 'superuser_dashboard.html')
    
    if request.user.is_authenticated:
        return render(request, 'volunteer_dashboard.html')
    
    return redirect('login')

from django.shortcuts import render, redirect

from events.views import group_events
from events.models import Event

import datetime


def dashboard_view(request, sorting='by-date'):
    user = request.user

    if user.is_authenticated:
        if user.is_superuser:
            if sorting == 'by-date':
                grouped_events = group_events('start_date')
                return render(request, 'dashboard/dashboard_superuser_by_date.html', {'grouped_events': grouped_events})

            elif sorting == 'by-venue':
                grouped_events = group_events('venue')
                return render(request, 'dashboard/dashboard_superuser_by_venue.html', {'grouped_events': grouped_events})

            elif sorting == 'by-title':
                events = Event.objects.filter(start_date__gte=datetime.date.today())
                events = events.order_by('title', 'start_date')
                context = {'events': events}
                return render(request, 'dashboard/dashboard_superuser_by_title.html', context)

        else:
            if sorting == 'by-date':
                grouped_events = group_events('start_date')
                return render(request, 'dashboard/dashboard_volunteer_by_date.html', {'grouped_events': grouped_events})

            elif sorting == 'by-venue':
                grouped_events = group_events('venue')
                return render(request, 'dashboard/dashboard_volunteer_by_venue.html', {'grouped_events': grouped_events})

            elif sorting == 'by-title':
                events = Event.objects.filter(start_date__gte=datetime.date.today())
                events = events.order_by('title', 'start_date')
                context = {'events': events}
                return render(request, 'dashboard/dashboard_volunteer_by_title.html', context)

    return redirect('login')

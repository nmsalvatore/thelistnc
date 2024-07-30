from django.shortcuts import render, redirect

from events.views import group_events
from events.models import Event

import datetime


def dashboard_view(request, sorting='by-date'):
    template = ''
    context = {}
    grouped_events = []

    user = request.user

    if user.is_authenticated:
        if sorting == 'by-date':
            grouped_events = group_events('date')
            context = {'grouped_events': grouped_events}
        elif sorting == 'by-venue':
            grouped_events = group_events('venue')
            context = {'grouped_events': grouped_events}
        elif sorting == 'by-title':
            events = Event.objects.filter(start_date__gte=datetime.date.today()).order_by("title", "start_date", "start_time")
            context = {'events': events}

        if user.is_superuser:
            if sorting == 'by-date':
                template = 'dashboard/dashboard_superuser_by_date.html'
            elif sorting == 'by-venue':
                template = 'dashboard/dashboard_superuser_by_venue.html'
            elif sorting == 'by-title':
                template = 'dashboard/dashboard_superuser_by_title.html'

        else:
            if sorting == 'by-date':
                template = 'dashboard/dashboard_volunteer_by_date.html'
            elif sorting == 'by-venue':
                template = 'dashboard/dashboard_volunteer_by_venue.html'
            elif sorting == 'by-title':
                template = 'dashboard/dashboard_volunteer_by_title.html'

        return render(request, template, context)

    else:
        return redirect('login')

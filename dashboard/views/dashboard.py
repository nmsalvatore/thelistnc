from django.shortcuts import render, redirect

from events.views import group_events
from events.models import Event

import datetime


def dashboard_view(request, sorting='by-date'):
    template = ''
    grouped_events = []

    user = request.user

    if user.is_authenticated:
        if sorting == 'by-date':
            grouped_events = group_events('date')
        elif sorting == 'by-venue':
            grouped_events = group_events('venue')
        elif sorting == 'by-title':
            grouped_events = group_events('title')

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

        context = {'grouped_events': grouped_events}
        return render(request, template, context)

    else:
        return redirect('login')

from django.shortcuts import render, redirect
from events.models import Event

import datetime


def dashboard_view(request, sorting='by-date'):
    user = request.user

    if user.is_authenticated:
        if user.is_superuser:
            if sorting == 'by-date':
                grouped_events = group_events('start_date')
                return render(request, 'dashboard_superuser_by_date.html', {'grouped_events': grouped_events})

            elif sorting == 'by-venue':
                grouped_events = group_events('venue')
                return render(request, 'dashboard_superuser_by_venue.html', {'grouped_events': grouped_events})
            
            elif sorting == 'by-title':
                events = Event.objects.filter(start_date__gte=datetime.date.today())
                events = events.order_by('title', 'start_date')
                context = {'events': events}
                return render(request, 'dashboard_superuser_by_title.html', context)

        else:
            if sorting == 'by-date':
                grouped_events = group_events('start_date')
                return render(request, 'dashboard_volunteer_by_date.html', {'grouped_events': grouped_events})

            elif sorting == 'by-venue':
                grouped_events = group_events('venue')
                return render(request, 'dashboard_volunteer_by_venue.html', {'grouped_events': grouped_events})
            
            elif sorting == 'by-title':
                events = Event.objects.filter(start_date__gte=datetime.date.today())
                events = events.order_by('title', 'start_date')
                context = {'events': events}
                return render(request, 'dashboard_volunteer_by_title.html', context)
    
    return redirect('login')


def group_events(field):
    events = Event.objects.filter(start_date__gte=datetime.date.today())
    events = events.order_by(field)

    grouped_events = []

    if field == 'start_date':
        dates = events.dates('start_date', 'day')
        for date in dates:
            date_events = events.filter(start_date=date)
            grouped_events.append((date, date_events))

    if field == 'venue':
        venues = events.values_list('venue', flat=True).distinct()
        for venue in venues:
            venue_events = events.filter(venue=venue).order_by('start_date', 'title')
            grouped_events.append((venue, venue_events))

    return grouped_events

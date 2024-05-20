from django.shortcuts import render
from .models import Event

import datetime


def the_list(request, sorting='by-date'):
    if sorting == 'by-date':
        grouped_events = group_events('start_date')
        context = {'grouped_events': grouped_events}
        return render(request, 'events/event_list_by_date.html', context)

    elif sorting == 'by-venue':
        grouped_events = group_events('venue')
        context = {'grouped_events': grouped_events}
        return render(request, 'events/event_list_by_venue.html', context)

    elif sorting == 'by-title':
        events = Event.objects.filter(start_date__gte=datetime.date.today())
        events = events.order_by('title', 'start_date')
        context = {'events': events}
        return render(request, 'events/event_list_by_title.html', context)


def group_events(field):
    events = Event.objects.filter(start_date__gte=datetime.date.today())
    events = events.order_by(field)

    grouped_events = []

    if field == 'start_date':
        dates = events.dates('start_date', 'day')
        for date in dates:
            date_events = events.filter(start_date=date).order_by('start_time', 'end_time')
            grouped_events.append((date, date_events))

    if field == 'venue':
        venues = events.values_list('venue', 'city').distinct()
        for venue_data in venues:
            venue = f'{venue_data[0]}, {venue_data[1]}'
            venue_events = events.filter(venue=venue_data[0], city=venue_data[1]).order_by('start_date', 'start_time', 'end_time')
            grouped_events.append((venue, venue_events))

    return grouped_events

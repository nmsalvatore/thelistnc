from django.shortcuts import render
from django.db.models.functions import Lower

from .models import Event

import datetime


def the_list(request, sorting='by-date'):
    if sorting == 'by-date':
        grouped_events = group_events('date')
        context = {'grouped_events': grouped_events}
        return render(request, 'events/event_list_by_date.html', context)

    elif sorting == 'by-venue':
        grouped_events = group_events('venue')
        context = {'grouped_events': grouped_events}
        return render(request, 'events/event_list_by_venue.html', context)

    elif sorting == 'by-title':
        grouped_events = group_events('title')
        context = {'grouped_events': grouped_events}
        return render(request, 'events/event_list_by_title.html', context)


def group_events(field):
    events = Event.objects.filter(start_date__gte=datetime.date.today())
    grouped_events = []

    if field == 'date':
        events = events.order_by('start_date')
        dates = events.dates('start_date', 'day')
        for date in dates:
            date_events = events.filter(start_date=date).order_by('start_time', 'end_time')
            grouped_events.append((date, date_events))

    if field == 'venue':
        events = events.order_by(Lower('venue'))
        venues = events.values_list('venue', 'city').distinct()
        for venue_data in venues:
            venue = f'{venue_data[0]}, {venue_data[1]}'
            venue_events = events.filter(venue=venue_data[0], city=venue_data[1]).order_by('start_date', 'start_time', 'end_time')
            grouped_events.append((venue, venue_events))

    if field == 'title':
        events = events.order_by(Lower('title'))
        titles = events.values_list('title', flat=True).distinct()
        for title in titles:
            title_events = events.filter(title=title).order_by('start_date', 'start_time', 'end_time')
            grouped_events.append((title, title_events))

    return grouped_events

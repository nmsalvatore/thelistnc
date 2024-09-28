from django.shortcuts import render
from django.db.models.functions import Lower

from .models import Event

import datetime


def the_list(request, sorting='by-date'):
    request.session['last_visited'] = request.get_full_path()

    if sorting == 'by-date':
        grouped_events = group_events('date')
        dates = Event.objects.filter(start_date__gte=datetime.date.today()).values_list('start_date', flat=True).distinct().order_by('start_date')
        context = {'grouped_events': grouped_events, 'dates': dates}
        return render(request, 'events/event_list_by_date.html', context)

    elif sorting == 'by-venue':
        grouped_events = group_events('venue')
        venues = Event.objects.filter(start_date__gte=datetime.date.today()).values_list('venue', flat=True).distinct().order_by('venue')
        sorted_venues = sorted(venues, key=natural_sort_key)
        context = {'grouped_events': grouped_events, 'venues': sorted_venues}
        return render(request, 'events/event_list_by_venue.html', context)

    elif sorting == 'by-title':
        grouped_events = group_events('title')
        titles = Event.objects.filter(start_date__gte=datetime.date.today()).values_list('title', flat=True).distinct()
        sorted_titles = sorted(titles, key=natural_sort_key)
        context = {'grouped_events': grouped_events, 'titles': sorted_titles}
        return render(request, 'events/event_list_by_title.html', context)


def group_events(field):
    events = Event.objects.filter(start_date__gte=datetime.date.today())
    grouped_events = []

    if field == 'date':
        events = events.order_by('start_date')
        dates = events.dates('start_date', 'day')
        for date in dates:
            date_events = events.filter(start_date=date).order_by('start_time', 'end_time', 'title')
            num_events = len(date_events)
            grouped_events.append((date, date_events, num_events))

    if field == 'venue':
        events = events.order_by(Lower('venue'))
        venue_details = events.values_list('venue', 'city').distinct()
        sorted_venue_details = sorted(venue_details, key=natural_sort_key)
        for details in sorted_venue_details:
            venue = details[0]
            city = details[1]
            venue_events = events.filter(venue=venue).order_by('start_date', 'start_time', 'end_time')
            num_events = len(venue_events)
            grouped_events.append((venue, venue_events, num_events, city))

    if field == 'title':
        events = events.order_by(Lower('title'))
        titles = events.values_list('title', flat=True).distinct()
        sorted_titles = sorted(titles, key=natural_sort_key)
        for title in sorted_titles:
            title_events = events.filter(title=title).order_by('start_date', 'start_time', 'end_time')
            num_events = len(title_events)
            grouped_events.append((title, title_events, num_events))

    return grouped_events


def natural_sort_key(value):
    name = value[0].lower() if isinstance(value, tuple) else value.lower()
    articles = {'the', 'a', 'an'}
    for article in articles:
        if name.startswith(article + ' '):
            name = name[len(article)+1:]
    return (name, value[1]) if isinstance(value, tuple) else name

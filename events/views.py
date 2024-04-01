from django.shortcuts import render
from .models import Event


def event_list_by_date(request):
    events = Event.objects.order_by('start_date')
    dates = events.dates('start_date', 'day')

    grouped_events = []
    for date in dates:
        date_events = events.filter(start_date__date=date)
        grouped_events.append((date, date_events))

    context = {
        'grouped_events': grouped_events
    }

    return render(request, 'event_list_by_date.html', context)


def event_list_by_venue(request):
    events = Event.objects.order_by('venue')
    venues = events.values_list('venue', flat=True).distinct()

    grouped_events = []
    for venue in venues:
        venue_events = events.filter(venue=venue)
        grouped_events.append((venue, venue_events))

    context = {
        'grouped_events': grouped_events
    }

    return render(request, 'event_list_by_venue.html', context)

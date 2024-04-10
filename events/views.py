from django.shortcuts import render
from .models import Event


def the_list(request, sorting='by-date'):
    if sorting == 'by-date':
        grouped_events = group_events('start_date')
        context = {'grouped_events': grouped_events}
        return render(request, 'event_list_by_date.html', context)

    elif sorting == 'by-venue':
        grouped_events = group_events('venue')
        context = {'grouped_events': grouped_events}
        return render(request, 'event_list_by_venue.html', context)


def group_events(field):
    grouped_events = []
    events = Event.objects.order_by(field)

    if field == 'start_date':
        dates = events.dates('start_date', 'day')
        for date in dates:
            date_events = events.filter(start_date__date=date)
            grouped_events.append((date, date_events))

    if field == 'venue':
        venues = events.values_list('venue', flat=True).distinct()
        for venue in venues:
            venue_events = events.filter(venue=venue).order_by('start_date')
            grouped_events.append((venue, venue_events))

    return grouped_events

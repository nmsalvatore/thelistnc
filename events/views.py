from django.shortcuts import render
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Event

import datetime
import re


def the_list(request, sorting='by-date'):
    full_path = request.get_full_path()
    request.session['last_visited'] = full_path
    search_query = request.GET.get("search", "").strip()

    sort_match = re.search(r'by-[a-zA-Z]+', full_path)
    if sort_match:
        sorting = sort_match.group()

    events = get_events(search_query)
    hx_request = request.headers.get("HX-Request")
    template_dir = "events/partials" if hx_request else "events"

    context = {
        "hx_request": hx_request,
        "sorting": sorting,
        "search_query": search_query
    }

    if sorting == 'by-date':
        grouped_events = group_events(events, 'date')
        dates = events.values_list('start_date', flat=True).distinct().order_by('start_date')
        context["dates"] = dates

    elif sorting == 'by-venue':
        grouped_events = group_events(events, 'venue')
        venues = events.values_list('venue', flat=True).distinct().order_by('venue')
        sorted_venues = sorted(venues, key=natural_sort_key)
        context["venues"] = sorted_venues

    elif sorting == 'by-title':
        grouped_events = group_events(events, 'title')
        titles = events.values_list('title', flat=True).distinct()
        sorted_titles = sorted(titles, key=natural_sort_key)
        context["titles"] = sorted_titles

    context["grouped_events"] = grouped_events
    template = f"{template_dir}/event_list_{sorting.replace('-', '_')}.html"
    response = render(request, template, context)
    response["Vary"] = "HX-Request"
    return response


def get_events(search_query):
    events = Event.objects.filter(start_date__gte=datetime.date.today())
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(venue__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    return events


def group_events(events, group_by):
    grouped_events = []

    if group_by == 'date':
        events = events.order_by('start_date')
        dates = events.dates('start_date', 'day')
        for date in dates:
            date_events = events.filter(start_date=date).order_by('start_time', 'end_time', 'title')
            num_events = len(date_events)
            grouped_events.append((date, date_events, num_events))

    if group_by == 'venue':
        events = events.order_by(Lower('venue'))
        venue_details = events.values_list('venue', 'city').distinct()
        sorted_venue_details = sorted(venue_details, key=natural_sort_key)
        for details in sorted_venue_details:
            venue = details[0]
            city = details[1]
            venue_events = events.filter(venue=venue).order_by('start_date', 'start_time', 'end_time')
            num_events = len(venue_events)
            grouped_events.append((venue, venue_events, num_events, city))

    if group_by == 'title':
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

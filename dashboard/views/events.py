from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from django.utils.text import slugify
from django.db import transaction
from accounts.forms import EventForm
from events.models import Event
from datetime import timedelta


def new_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EventForm(request.POST)

            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                title = form.cleaned_data['title']

                if end_date:
                    events = []
                    current_date = start_date

                    while current_date <= end_date:
                        event_data = {
                            **form.cleaned_data,
                            'continuous': False,
                            'manual_upload': True,
                            'start_date': current_date,
                            'end_date': None,
                            'created_by': request.user,
                        }

                        event = Event(**event_data)
                        events.append(event)
                        current_date += timedelta(days=1)

                    with transaction.atomic():
                        Event.objects.bulk_create(events)

                else:
                    new_event = form.save(commit=False)
                    new_event.created_by = request.user
                    new_event.manual_upload = True
                    new_event.save()

                redirect_path = get_redirect_path(request, form=form)
                return redirect(redirect_path)

        else:
            form = EventForm()
            context = {'form': form}
            return render(request, 'dashboard/event_form_new.html', context)

    else:
        raise Http404('Page not found')


def template_event(request, uuid):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(uuid=uuid)
        except:
            raise Http404('Event not found')

        if request.method == 'POST':
            form = EventForm(request.POST)

            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']

                if end_date:
                    events = []
                    current_date = start_date

                    while current_date <= end_date:
                        event_data = {
                            **form.cleaned_data,
                            'continuous': False,
                            'manual_upload': True,
                            'start_date': current_date,
                            'end_date': None,
                            'created_by': request.user,
                        }

                        event = Event(**event_data)
                        events.append(event)
                        current_date += timedelta(days=1)

                    with transaction.atomic():
                        Event.objects.bulk_create(events)

                else:
                    new_event = form.save(commit=False)
                    new_event.created_by = request.user
                    new_event.manual_upload = True
                    new_event.save()

                redirect_path = get_redirect_path(request, form=form)
                return redirect(redirect_path)

        else:
            form = EventForm(instance=event)
            context = {'form': form}
            return render(request, 'dashboard/event_form_new.html', context)

    else:
        raise Http404('Page not found')


def edit_event(request, uuid):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(uuid=uuid)
        except:
            raise Http404('Event not found')

        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)

            if form.is_valid():
                new_event = form.save(commit=False)
                new_event.created_by = request.user
                new_event.manual_upload = True
                new_event.save()

                redirect_path = get_redirect_path(request, form=form)
                return redirect(redirect_path)
        else:
            form = EventForm(instance=event)

        context = {'form': form, 'uuid': uuid}
        return render(request, 'dashboard/event_form_edit.html', context)

    else:
        raise Http404('Page not found')


def delete_event(request, uuid):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(uuid=uuid)
            redirect_path = get_redirect_path(request, event=event)
        except:
            raise Http404('Event not found')

        event.delete()
        return redirect(redirect_path)
    else:
        raise Http404('Page not found')


# helper functions

def create_new_event(request, form):
    form = EventForm(request.POST)

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if end_date:
            events = []
            current_date = start_date

            while current_date <= end_date:
                event_data = {
                    **form.cleaned_data,
                    'start_date': current_date,
                    'created_by': request.user,
                }

                event = Event(**event_data)
                events.append(event)
                current_date += timedelta(days=1)

            with transaction.atomic():
                Event.objects.bulk_create(events)

        else:
            new_event = form.save(commit=False)
            new_event.created_by = request.user
            new_event.save()


def get_redirect_path(request, form=None, event=None):
    last_visited = request.session.get('last_visited')

    if not last_visited:
        return "home"

    element_id = ""

    if 'by-date' in last_visited:
        date = ""
        if form:
            date = form.cleaned_data['start_date']
        elif event:
            date = event.start_date
        element_id = str(date).replace("-", "")

    if 'by-venue' in last_visited:
        venue = ""
        if form:
            venue = form.cleaned_data['venue']
        elif event:
            venue = event.venue
        element_id = slugify(venue)

    if 'by-title' in last_visited:
        title = ""
        if form:
            title = form.cleaned_data['title']
        elif event:
            title = event.title
        element_id = slugify(title)

    return last_visited + f'#events_{element_id}'

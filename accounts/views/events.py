from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
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
                    
                    return redirect(reverse('dashboard', args=['by-date']))
                else:
                    new_event = form.save(commit=False)
                    new_event.created_by = request.user
                    new_event.save()
                    return redirect(reverse('dashboard', args=['by-date']))

        else:
            form = EventForm()
            context = {'form': form}
            return render(request, 'event_form_new.html', context)

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
                new_event = form.save(commit=False)
                new_event.created_by = request.user
                new_event.save()
                return redirect(reverse('dashboard', args=['by-date']))

        else:
            form = EventForm(instance=event)

        context = {'form': form}
        return render(request, 'event_form_new.html', context)

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
                new_event.save()
                return redirect(reverse('dashboard', args=['by-date']))
        else:
            form = EventForm(instance=event)

        context = {'form': form, 'uuid': uuid}
        return render(request, 'event_form_edit.html', context)

    else:
        raise Http404('Page not found')


def delete_event(request, uuid):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(uuid=uuid)
        except:
            raise Http404('Event not found')
        
        event.delete()
        return redirect(reverse('dashboard', args=['by-date']))
    else:
        raise Http404('Page not found')

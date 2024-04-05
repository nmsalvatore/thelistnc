from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from accounts.forms import EventForm
from events.models import Event


def new_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EventForm(request.POST)

            if form.is_valid():
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

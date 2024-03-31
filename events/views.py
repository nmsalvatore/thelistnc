from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'events/event_list.html', context)
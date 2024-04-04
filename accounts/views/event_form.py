from django.shortcuts import render, redirect
from django.http import Http404
from accounts.forms import EventForm


def event_form_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EventForm(request.POST)
            print('id', request.user)

            if form.is_valid():
                new_event = form.save(commit=False)
                new_event.created_by = request.user
                new_event.save()
                return redirect('home')

        else:
            form = EventForm()
            context = {'form': form}
            return render(request, 'event_form.html', context)
    else:
        raise Http404('Page not found')

from django.urls import path
from .views import event_list_by_date, event_list_by_venue

urlpatterns = [
    path('by-date/', event_list_by_date, name='event_list_by_date'),
    path('by-venue/', event_list_by_venue, name='event_list_by_venue')
]

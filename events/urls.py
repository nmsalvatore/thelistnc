from django.urls import path, include
from .views import event_list

urlpatterns = [
    path('', event_list, name='event-list')
]

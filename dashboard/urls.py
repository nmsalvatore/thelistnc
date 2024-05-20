from django.urls import path

from dashboard.views.dashboard import dashboard_view
from dashboard.views.events import new_event, edit_event, delete_event, template_event
from dashboard.views.admin import admin


urlpatterns = [
    path('event/new/', new_event, name='new_event_form'),
    path('event/new/<uuid:uuid>', template_event, name='template_event_form'),
    path('event/edit/<uuid:uuid>/', edit_event, name='edit_event_form'),
    path('event/delete/<uuid:uuid>/', delete_event, name='delete_event'),
    path('events/<str:sorting>/', dashboard_view, name='dashboard'),
    path('', admin, name='admin')
]

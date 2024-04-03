from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

from events.views import event_list_by_date
from .views import custom_404

handler404 = custom_404

urlpatterns = [
    path('', event_list_by_date, name='home'),
    path('django-admin/', admin.site.urls),
    path('admin/', include('accounts.urls')),
    path('events/', include('events.urls')),
]

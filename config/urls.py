from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

from events.views import the_list
from .views import custom_404

handler404 = custom_404

urlpatterns = [
    path('', the_list, name='home'),
    path('django-admin/', admin.site.urls),
    path('admin/', include('accounts.urls')),
    path('events/', include('events.urls')),
]

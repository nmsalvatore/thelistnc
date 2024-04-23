from django.contrib import admin
from django.urls import path, include
from events.views import the_list


urlpatterns = [
    path('', the_list, name='home'),
    path('django-admin/', admin.site.urls),
    path('admin/', include('accounts.urls')),
    path('events/', include('events.urls')),
]

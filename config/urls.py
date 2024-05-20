from django.contrib import admin
from django.urls import path, include
from events.views import the_list


urlpatterns = [
    path('', the_list, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('dashboard/', include('dashboard.urls')),
]

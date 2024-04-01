from django.contrib import admin
from django.urls import path, include

from events.views import event_list_by_date

urlpatterns = [
    path('', event_list_by_date, name='home'),
    path('admin/', admin.site.urls),
    path('moderator/', include('accounts.urls')),
    path('events/', include('events.urls')),
]

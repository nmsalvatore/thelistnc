from django.contrib import admin
from django.urls import path, include

from events.views import the_list
from .views import RobotsTxtView


urlpatterns = [
    path('', the_list, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('robots.txt', RobotsTxtView.as_view(content_type='text/plain'), name='robots')
]

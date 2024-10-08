from django.contrib import admin
from django.urls import path, include

from .views import home, RobotsTxtView


urlpatterns = [
    path('', home, name='home'),
    path('django-admin/', admin.site.urls),
    path('admin/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('robots.txt', RobotsTxtView.as_view(content_type='text/plain'), name='robots')
]

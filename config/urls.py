from django.contrib import admin
from django.urls import path, include, re_path

from .views import FarewellView, RobotsTxtView, catch_all


urlpatterns = [
    re_path(r'^(?!$).+', catch_all),
    path('', FarewellView.as_view(), name="farewell"),
    path('django-admin/', admin.site.urls),
    path('admin/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('robots.txt', RobotsTxtView.as_view(content_type='text/plain'), name='robots')
]

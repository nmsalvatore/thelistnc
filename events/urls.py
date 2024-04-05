from django.urls import path
from .views import the_list

urlpatterns = [
    path('<str:sorting>/', the_list, name='the_list')
]

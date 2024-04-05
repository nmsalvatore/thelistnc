from django.urls import path

from accounts.views.invitation import send_invitation, invitation_sent
from accounts.views.register import register_view, verify_register_otp, registration_success
from accounts.views.login import login_view, verify_login_otp
from accounts.views.logout import logout_view
from accounts.views.dashboard import dashboard_view
from accounts.views.events import new_event, edit_event, delete_event
from accounts.views.admin import admin


urlpatterns = [
    path('send-invitation/', send_invitation, name='send_invitation'),
    path('invitation-sent/', invitation_sent, name='invitation_sent'),
    path('register/', register_view, name='register'),
    path('register/verify/', verify_register_otp, name='verify_register_otp'),
    path('register/success/', registration_success, name='registration_success'),
    path('login/', login_view, name='login'),
    path('login/verify/', verify_login_otp, name='verify_login_otp'),
    path('logout/', logout_view, name='logout'),
    path('event/new/', new_event, name='new_event_form'),
    path('event/edit/<uuid:uuid>/', edit_event, name='edit_event_form'),
    path('event/delete/<uuid:uuid>/', delete_event, name='delete_event'),
    path('<str:sorting>/', dashboard_view, name='dashboard'),
    path('', admin, name='admin')
]

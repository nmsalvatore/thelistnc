from django.urls import path

from accounts.views.invitation import send_invitation, invitation_sent
from accounts.views.register import register_view, verify_register_otp, registration_success
from accounts.views.login import login_view, verify_login_otp
from accounts.views.logout import logout_view
from accounts.views.dashboard import dashboard_view
from accounts.views.event_form import event_form_view


urlpatterns = [
    path('send-invitation/', send_invitation, name='send_invitation'),
    path('invitation-sent/', invitation_sent, name='invitation_sent'),
    path('register/', register_view, name='register'),
    path('register/verify/', verify_register_otp, name='verify_register_otp'),
    path('register/success/', registration_success, name='registration_success'),
    path('login/', login_view, name='login'),
    path('login/verify/', verify_login_otp, name='verify_login_otp'),
    path('logout/', logout_view, name='logout'),
    path('event/new/', event_form_view, name='event_form'),
    path('', dashboard_view, name='dashboard'),
]

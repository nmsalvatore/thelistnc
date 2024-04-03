from django.urls import path

from accounts.views.invitation import send_invitation, invitation_sent
from accounts.views.register import register_view, verify_register_otp, registration_success
from accounts.views.login import login_view, verify_login_otp
from accounts.views.logout import logout_view
from accounts.views.dashboard import dashboard_view


urlpatterns = [
    path('send-invitation/', send_invitation, name='send_invitation'),
    path('invitation-sent/', invitation_sent, name='invitation_sent'),
    path('register/', register_view, name='register'),
    path('registration-success/', registration_success, name='registration_success'),
    path('verify-register-otp/', verify_register_otp, name='verify_register_otp'),
    path('verify-login-otp/', verify_login_otp, name='verify_login_otp'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', dashboard_view, name='dashboard'),
]

from django.urls import path
from .admin_views import send_invitation, invitation_sent
from .views import register, registration_success, verify_otp, verify_login_otp, login_view, logout_view

urlpatterns = [
    path('send-invitation/', send_invitation, name='send_invitation'),
    path('invitation-sent/', invitation_sent, name='invitation_sent'),
    path('register/', register, name='register'),
    path('registration-success/', registration_success, name='registration_success'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('verify-login-otp/', verify_login_otp, name='verify_login_otp'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
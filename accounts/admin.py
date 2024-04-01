from django.contrib import admin
from .models import UserProfile, Invitation

admin.site.register(UserProfile)
admin.site.register(Invitation)
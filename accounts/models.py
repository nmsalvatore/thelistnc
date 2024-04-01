from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='moderator')

    def __str__(self):
        return self.user.username


class Invitation(models.Model):
    email = models.EmailField(unique=True)
    code = models.UUIDField(default=uuid4, unique=True, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

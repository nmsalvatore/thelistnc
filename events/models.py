import uuid

from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    admission_price = models.CharField(max_length=255, blank=True, null=True)
    venue = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    start_date = models.DateField()
    start_time = models.TimeField(null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    url = models.URLField(max_length=300, blank=True, null=True)
    continuous = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_info = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='events', null=True)
    manual_upload = models.BooleanField(default=False)

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings
from django.utils.timesince import timesince
import uuid
from django.utils import timezone
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None



class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    message = models.TextField()
    icon = models.CharField(max_length=50, default='bell')  # Optional: "bell", "check", "alert"
    image = models.ImageField(upload_to='notifications/', null=True, blank=True)
    url = models.URLField(default='#')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    def time_ago(self):
        return timesince(self.created_at) + ' ago'

    def __str__(self):
        return f"{self.user} - {self.message[:30]}"

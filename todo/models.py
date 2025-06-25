from django.db import models
from django.conf import settings
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None



from staff.models import Staff

from django.utils import timezone
import uuid


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    task_date = models.DateField(null=True)
    finish_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    TASK_TYPE_CHOICES = (
        (0, 'General'),
        (1, 'Urgent'),
        (2, 'Immediate'),
    )
    task_type = models.IntegerField(choices=TASK_TYPE_CHOICES, default=0, null=True, blank=True)

    TASK_REPEAT_CHOICES = (
        (0, 'One Time'),
        (1, 'Every Day'),
        (2, 'Every Week'),
        (3, 'Every Month'),
        (4, 'Every Year'),
    )
    task_repeat = models.IntegerField(choices=TASK_REPEAT_CHOICES, default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.task_name} ({self.get_task_type_display()})"


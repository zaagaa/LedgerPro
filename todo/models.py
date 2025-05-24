from django.db import models
from django.conf import settings

from staff.models import Staff

from django.utils import timezone


class Task(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    task_date = models.DateField(null=True)
    finish_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)

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

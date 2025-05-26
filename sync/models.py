from django.db import models
from django.utils import timezone

class Deleted_Record(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    app_name=models.CharField(max_length=100, null=True, blank=True)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    model_id = models.IntegerField(null=True, blank=True)
    deleted = models.IntegerField(default=0, null=True, blank=True)




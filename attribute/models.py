from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None




from django.db import models

from company.models import Company
from datetime import *
from django.utils import timezone
import uuid



class Attribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    attribute_name=models.CharField(max_length=100)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)



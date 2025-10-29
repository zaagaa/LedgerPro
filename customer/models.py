from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None



from django.db import models
from django.utils import timezone

from authentication.models import User
import uuid


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    customer_name=models.CharField(max_length=50)
    tax_number=models.CharField(max_length=50, null=True, blank=True)
    address=models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    # mobile = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    mobile = models.BigIntegerField(null=True, blank=True, db_index=True)
    point = models.FloatField(default=0, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)






from django.db import models
from django.conf import settings
from django.utils import timezone
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None


from company.models import Company
from django.utils import timezone
from datetime import datetime
import uuid


class Expenses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    amount = models.FloatField(default=0, null=True, blank=True)
    description=models.CharField(max_length=100, null=True, blank=True)
    entry_date = models.DateTimeField(default=datetime.now, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)




class Cash_Flow_Expenses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    amount = models.FloatField(default=0, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    entry_date = models.DateTimeField(default=datetime.now, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)



    def __str__(self):
        return f"{self.entry_date.strftime('%d-%m-%Y')} - ₹{self.amount} - {self.description}"


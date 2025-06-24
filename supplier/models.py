from django.db import models
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
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django_countries.fields import CountryField
import uuid

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    supplier_name=models.CharField(max_length=150)
    tax_number=models.CharField(max_length=150, null=True)
    address=models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = CountryField(max_length=200, blank_label='(Select Country)', null=True)  # Use CountryField here
    pincode = models.CharField(max_length=200, null=True)
    mobile = models.BigIntegerField(default=None, null=True)
    code_name = models.CharField(max_length=20, null=True, blank=True)
    default_margin = models.CharField(max_length=20, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)



class Bundle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    supplier=models.ForeignKey('Supplier', on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    entry_date = models.DateTimeField(default=datetime.now, blank=True)
    qty = models.IntegerField(default=0, null=True, blank=True)
    transport = models.CharField(max_length=50, null=True, blank=True)
    transport_charge = models.FloatField(default=0, null=True, blank=True)
    service_charge = models.FloatField(default=0, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)






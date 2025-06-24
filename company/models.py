from django.db import models
from django.utils import timezone  # Import timezone from django.utils
from django_countries.fields import CountryField
import uuid
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None



class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company_name = models.CharField(max_length=150, null=True)
    tax_number = models.CharField(max_length=150, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = CountryField(max_length=200, blank_label='(Select Country)', null=True)  # Use CountryField here
    pincode = models.CharField(max_length=200, null=True)
    TAX_CHOICES = [
        ('Gst', 'GST'),
        ('Vat', 'VAT'),
    ]
    tax_type = models.CharField(max_length=10, choices=TAX_CHOICES, null=True)
    mobile = models.BigIntegerField(default=None, null=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)


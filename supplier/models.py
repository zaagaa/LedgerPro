from django.db import models
from django.utils import timezone

from company.models import Company
from django.conf import settings
from datetime import datetime
from django_countries.fields import CountryField

class Supplier(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
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



class Bundle(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier=models.ForeignKey('Supplier', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)
    entry_date = models.DateTimeField(default=datetime.now, blank=True)
    qty = models.IntegerField(default=0, null=True, blank=True)
    transport = models.CharField(max_length=50, null=True, blank=True)
    transport_charge = models.FloatField(default=0, null=True, blank=True)
    service_charge = models.FloatField(default=0, null=True, blank=True)





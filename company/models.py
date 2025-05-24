from django.db import models
from django.utils import timezone  # Import timezone from django.utils
from django_countries.fields import CountryField

class Company(models.Model):
    TAX_CHOICES = [
        ('Gst', 'GST'),
        ('Vat', 'VAT'),
    ]
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)  # Use timezone.now
    company_name = models.CharField(max_length=150, null=True)
    tax_number = models.CharField(max_length=150, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = CountryField(max_length=200, blank_label='(Select Country)', null=True)  # Use CountryField here
    pincode = models.CharField(max_length=200, null=True)
    tax_type = models.CharField(max_length=10, choices=TAX_CHOICES, null=True)
    mobile = models.BigIntegerField(default=None, null=True)

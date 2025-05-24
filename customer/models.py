
from django.db import models
from django.utils import timezone

from authentication.models import User


class Customer(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    customer_name=models.CharField(max_length=50)
    tax_number=models.CharField(max_length=50, null=True, blank=True)
    address=models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    mobile = models.BigIntegerField(unique=True, null=True, blank=True)
    point = models.FloatField(default=0, null=True, blank=True)





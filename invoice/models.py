from django.db import models
from django.utils import timezone

from company.models import Company
from customer.models import Customer
from inventory.models import Inventory
from purchase.models import Stock
from datetime import datetime
from django.conf import settings


class Invoice(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(default=datetime.now,blank=True)
    invoice_number = models.IntegerField(default=0, null=True, blank=True)
    total_amount = models.FloatField(default=0, null=True, blank=True)
    discount = models.CharField(max_length=10, null=True, blank=True)
    discount_value = models.FloatField(default=None, null=True, blank=True)
    exchange_value = models.FloatField(default=None, null=True, blank=True)
    cash = models.FloatField(default=None, null=True, blank=True)
    card = models.FloatField(default=None, null=True, blank=True)
    upi = models.FloatField(default=None, null=True, blank=True)
    credit = models.FloatField(default=None, null=True, blank=True)
    headline = models.CharField(max_length=100, null=True, blank=True)
    round_off=models.FloatField(default=None, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True, blank=True)
    invoice_type = models.IntegerField(default=0, null=True, blank=True)
    cancel_no = models.IntegerField(default=None, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['company']),  # Index on company_id
            models.Index(fields=['invoice_date']),  # Index on invoice_date
            models.Index(fields=['company', 'invoice_date']),  # Composite Index
        ]


class Point_Entry(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    entry_date = models.DateTimeField(default=datetime.now,blank=True)
    point = models.FloatField(default=0, null=True, blank=True)
    balance = models.FloatField(default=0, null=True, blank=True)
    description = models.CharField(max_length=75, null=True, blank=True)



class Sale(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    invoice=models.ForeignKey('Invoice', on_delete=models.CASCADE)
    stock=models.ForeignKey(Stock, on_delete=models.DO_NOTHING, null=True, blank=True)
    inventory=models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    tax_rate = models.FloatField(default=0)
    unit = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    sale_price = models.FloatField(default=0)
    discount=models.CharField(max_length=10, null=True, blank=True)
    actual_sale_price=models.FloatField(default=0)









from django.db import models
from django.conf import settings
from django.utils import timezone

from company.models import Company
from datetime import datetime


class Expenses(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, null=True, blank=True)
    description=models.CharField(max_length=100, null=True, blank=True)
    entry_date = models.DateTimeField(default=datetime.now, blank=True)


class Cash_Flow_Expenses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    entry_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.entry_date.strftime('%d-%m-%Y')} - ₹{self.amount} - {self.description}"

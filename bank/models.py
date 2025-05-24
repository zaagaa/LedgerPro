from django.db import models

from company.models import Company
from purchase.models import Payment
from supplier.models import Supplier
from datetime import *
from django.utils import timezone



class Bank_Account(models.Model):
    sync=models.DateTimeField(default=timezone.now, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    ac_name = models.CharField(max_length=50, null=True, blank=True)
    ac_no = models.CharField(max_length=50, null=True, blank=True)
    ac_type = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    ifsc = models.CharField(max_length=50, null=True, blank=True)

class Bank_Statement(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    bank_account = models.ForeignKey('Bank_Account', on_delete=models.DO_NOTHING, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True, blank=True)
    tran_id = models.CharField(max_length=50, null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    cheque_no = models.CharField(max_length=50, null=True, blank=True)
    ref_no = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    debit = models.FloatField(null=True, blank=True)
    credit = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('company', 'bank_account', 'tran_id', 'entry_date', 'balance')



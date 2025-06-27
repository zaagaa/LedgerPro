from django.db import models
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None



from company.models import Company
from purchase.models import Payment
from supplier.models import Supplier
from datetime import *
from django.utils import timezone
import uuid



class Bank_Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    ac_name = models.CharField(max_length=50, null=True, blank=True)
    ac_no = models.CharField(max_length=50, null=True, blank=True)
    ac_type = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    ifsc = models.CharField(max_length=50, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

class Bank_Statement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    bank_account = models.ForeignKey('Bank_Account', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    tran_id = models.CharField(max_length=50, null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    cheque_no = models.CharField(max_length=50, null=True, blank=True)
    ref_no = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    debit = models.FloatField(null=True, blank=True)
    credit = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    class Meta:
        unique_together = ('company', 'bank_account', 'tran_id', 'entry_date', 'balance')




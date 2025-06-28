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

from tax_code.models import Tax_Code
import uuid

class Floor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    def __str__(self):
        return self.name

class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    def __str__(self):
        return f"{self.floor.name} → {self.name}"

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tax_code=models.ForeignKey(Tax_Code, on_delete=models.SET_NULL, null=True, db_index=True)
    inventory_name=models.CharField(max_length=200)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    shortcode=models.CharField(max_length=10, blank=True, null=True)
    unit_enabled=models.IntegerField(default=0)
    default_price=models.IntegerField(default=None, blank=True, null=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ('company', 'inventory_name', 'tax_code')

    def __str__(self):
        return self.inventory_name

    @property
    def tax_display(self):
        if self.tax_code:
            return f"{self.tax_code.tax_code} - {self.tax_code.tax_rate}%"
        return ''


class TaxSlab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    tax_rate = models.FloatField()
    trigger_amount = models.FloatField()
    inventories = models.ManyToManyField(Inventory, related_name='tax_slabs')
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    def __str__(self):
        return self.name


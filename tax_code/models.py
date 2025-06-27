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
from BusinessApp.function import int_value
import uuid


class Tax_Code(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    tax_code=models.IntegerField(default=0, null=True)
    tax_rate=models.IntegerField(default=0,null=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)


    class Meta:
        unique_together = ('company', 'tax_code')

    def __str__(self):
        return self.tax_code

    @property
    def tax_rate_view(self):
        return int_value(self.tax_rate)

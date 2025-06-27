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
import uuid


class Setting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    setting=models.CharField(max_length=100)
    value=models.CharField(max_length=1000)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    class Meta:
        unique_together = ('company', 'setting')  # Ensures the combination of company and setting is unique
        constraints = [
            models.UniqueConstraint(fields=['company', 'setting'], name='unique_company_setting', condition=models.Q(company__isnull=False))
        ]

    def __str__(self):
        return self.setting

class Master_Setting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    setting=models.CharField(max_length=50, unique=True)
    value=models.CharField(max_length=100)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)




from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None




from django.db import models
from django.utils import timezone


from company.models import Company
from django.conf import settings
import uuid




class Cash_Counter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    stand_by=models.CharField(max_length=100, null=True, blank=True)
    cash_taken = models.CharField(max_length=100, null=True, blank=True)
    entry_date = models.DateTimeField(null=True, blank=True)
    finish = models.IntegerField(default=0, null=True, blank=True)
    shortage=models.FloatField(default=None, null=True, blank=True)
    stand_by_total = models.FloatField(default=None, null=True, blank=True)
    cash_taken_total = models.FloatField(default=None, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)


class Print_Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    template_name = models.CharField(max_length=150, null=True, blank=True)
    template = models.TextField(null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)





#
# from django.db import models
# from django.conf import settings
# from django.utils import timezone
# import uuid
#
# class UnprintedSaleLog(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
#     session_id = models.CharField(max_length=100, db_index=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
#     row_number = models.IntegerField(null=True, blank=True)
#     stock = models.ForeignKey('purchase.Stock', on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
#     inventory = models.ForeignKey('inventory.Inventory', on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
#     unit = models.FloatField(default=0)
#     qty = models.FloatField(default=0)
#     sale_price = models.FloatField(default=0)
#     discount = models.CharField(max_length=10, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     visible_duration = models.IntegerField(default=0,
#                                            help_text="Duration in milliseconds the row was visible before print or refresh.")
#     sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
#     sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)
#
#     def __str__(self):
#         return f"{self.user.username} | {self.inventory} | {self.qty}"
#
# class FieldChangeLog(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
#     session_id = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     row_number = models.IntegerField()
#     field = models.CharField(max_length=50)
#     old_value = models.CharField(max_length=255, null=True, blank=True)
#     new_value = models.CharField(max_length=255, null=True, blank=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
#     sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)
#
#     def __str__(self):
#         return f"{self.user} - Row {self.row_number} changed {self.field}"

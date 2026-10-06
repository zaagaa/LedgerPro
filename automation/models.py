from django.db import models
import uuid
from django.conf import settings

from attribute.models import Attribute
from inventory.models import Inventory
from supplier.models import Supplier


def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None


class Stock_Order_Setting(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        null=True,
        db_index=True
    )

    minimum_stock = models.FloatField(
        default=0
    )

    maximum_stock = models.FloatField(
        default=0
    )

    per_box_contain = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None
    )

    enabled = models.BooleanField(
        default=True
    )

    sync_offline = models.BigIntegerField(
        null=True,
        blank=True,
        default=initial_sync_offline
    )

    sync_online = models.BigIntegerField(
        null=True,
        blank=True,
        default=initial_sync_online
    )



class Stock_Order_Setting_Attribute(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    stock_order_setting = models.ForeignKey(
        Stock_Order_Setting,
        on_delete=models.CASCADE,
        related_name="attributes",
        db_index=True
    )

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        null=True,
        db_index=True
    )

    sync_offline = models.BigIntegerField(
        null=True,
        blank=True,
        default=initial_sync_offline
    )

    sync_online = models.BigIntegerField(
        null=True,
        blank=True,
        default=initial_sync_online
    )


class Stock_Order_Brand_Setting(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        db_index=True
    )

    brand = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        db_index=True
    )

    default_supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )

    whatsapp_mobile = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    minimum_order_qty = models.FloatField(
        default=0
    )

    per_box_contain = models.PositiveIntegerField(
        default=1
    )

    enabled = models.BooleanField(
        default=True
    )

    sync_offline = models.BigIntegerField(
        null=True,
        blank=True,
        default=initial_sync_offline
    )

    sync_online = models.BigIntegerField(
        null=True,
        blank=True,
        default=initial_sync_online
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["inventory", "brand"],
                name="unique_stock_order_brand_setting"
            )
        ]


class Stock_Order_WhatsApp_Log(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    whatsapp_mobile = models.CharField(
        max_length=20
    )

    last_sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    last_items = models.JSONField(
        default=list,
        blank=True
    )

    last_message = models.TextField(
        blank=True,
        default=""
    )

    class Meta:
        unique_together = (
            "supplier",
            "whatsapp_mobile",
        )

    def __str__(self):
        return (
            f"{self.supplier} - "
            f"{self.whatsapp_mobile}"
        )
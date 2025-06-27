from datetime import *
from django.utils import timezone
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None



from django.db import models

from attribute.models import Attribute
from company.models import Company

from inventory.models import Inventory
from supplier.models import Supplier
from tax_code.models import Tax_Code
from BusinessApp.function import *
from django.conf import settings
import re
import uuid

class Sticker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    sticker_name = models.CharField(max_length=50, null=True, blank=True)
    column = models.IntegerField(default=0, null=True, blank=True)
    sticker_code = models.TextField(null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    amount=models.FloatField(default=0, null=True, blank=True)
    purchase = models.ForeignKey('Purchase', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    paid_by = models.CharField(max_length=15, null=True, blank=True)
    tran_no = models.CharField(max_length=100, null=True, blank=True)
    cheque_cleared = models.IntegerField(default=0, null=True, blank=True)
    cheque_given = models.IntegerField(default=0, null=True, blank=True)
    bank_checked = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    verify = models.IntegerField(default=None, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    def __str__(self):
        supplier_name = self.supplier.supplier_name if self.supplier else "No Supplier"
        date = self.transaction_date.strftime("%Y-%m-%d") if self.transaction_date else "No Date"
        return f"{supplier_name} | ₹{self.amount:.2f} on {date}"

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, db_index=True)
    invoice_number= models.CharField(max_length=25, null=True, blank=True)
    transaction_date= models.DateField(null=True, blank=True)
    discount= models.CharField(max_length=10, null=True, blank=True)
    round_off = models.FloatField(default=0, null=True, blank=True)
    other_charges = models.FloatField(default=0, null=True, blank=True)
    payable_amount= models.FloatField(default=0, null=True, blank=True)
    finish = models.IntegerField(default=0, null=True, blank=True)
    stock_only = models.IntegerField(default=0, null=True, blank=True)
    total_margin=models.FloatField(null=True, blank=True)
    verify = models.IntegerField(default=None, null=True, blank=True)
    finish_upload = models.BooleanField(default=False)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)


    @property
    def other_charges_view(self):
        return int_value(self.other_charges)

class Stock_Attribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    purchase = models.ForeignKey('Purchase', on_delete=models.CASCADE, null=True, db_index=True)
    stock=models.ForeignKey('Stock', on_delete=models.CASCADE, null=True, db_index=True)
    attribute=models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, db_index=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    # class Meta:
    #     unique_together = ('company', 'attribute', 'stock')
    #ON IT ONCE FRESH INSTALL


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # barcode=models.IntegerField(default=0, unique=True)
    barcode = models.BigIntegerField(unique=True)
    pre_barcode = models.CharField(max_length=550, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, db_index=True)
    # purchase=models.ForeignKey('Purchase', on_delete=models.CASCADE, null=True, db_index=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='stocks', null=True, db_index=True)
    tax_code = models.ForeignKey(Tax_Code, on_delete=models.SET_NULL, null=True, db_index=True)
    inventory=models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, db_index=True)
    tax_rate=models.FloatField(default=0)
    buy_price=models.FloatField(default=0)
    discount = models.CharField(max_length=10, null=True, blank=True)
    unit = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    sold = models.FloatField(default=0, null=True, blank=True)
    sale_price = models.FloatField(default=0)
    mrp = models.FloatField(default=0)
    sold = models.FloatField(default=0, null=True, blank=True)
    mfg_date=models.DateField(default=None, null=True, blank=True)
    exp_date = models.DateField(default=None, null=True, blank=True)
    best_before = models.CharField(max_length=50, null=True, blank=True)
    sticker = models.IntegerField(default=None, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)
    imported_stock = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['barcode']),      # Index on barcode
            models.Index(fields=['pre_barcode']),  # Index on pre_barcode
            models.Index(fields=['company']),      # Index on company (ForeignKey)
        ]

    @property
    def row_total(self):

        if self.discount=='':
            self.discount=0.00

        row_total=(self.buy_price * self.unit * self.qty)

        if self.discount is not None:
            if self.discount!=0 and self.discount!='0' and self.discount!=0.00:
                if "%" in self.discount:
                    discount_percent=self.discount.replace("%","")
                    row_total=row_total-(row_total*float(discount_percent)/100)
                else:
                    #print(self.discount,">>>>>")
                    row_total=((self.buy_price-float(self.discount)) * self.unit * self.qty)



        return (row_total)

    @property
    def margin(self):

        tax=self.tax_rate/100
        buy=self.buy_price+(self.buy_price*tax)

        return round((((self.sale_price/buy)*100)-100), 2)

    @property
    def margin_raw(self):

        tax=self.tax_rate/100
        buy=self.buy_price+(self.buy_price*tax)

        return (((self.sale_price/buy)*100)-100)

    @property
    def barcode_view(self):
        return f"{int(str(self.barcode)[:2])}A{int(str(self.barcode)[2:])}"

    @property
    def unit_view(self):
        return int_value(self.unit)

    @property
    def qty_view(self):
        return int_value(self.qty)

    @property
    def tax_rate_view(self):
        return int_value(self.tax_rate)

    @property
    def best_before_view(self):
        try:
            value = float(self.best_before)
            return f"{int(value)} Month"
        except (ValueError, TypeError):
            # Extract numeric part from self.best_before
            cleaned = re.sub(r"[^\d.]", "", str(self.best_before))
            return f"{cleaned} Days" if cleaned else ""



class PurchaseScan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    purchase = models.ForeignKey('Purchase', on_delete=models.CASCADE, related_name='scans', db_index=True)
    image = models.ImageField(upload_to='purchase_scans/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

class ColumnPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    columns = models.JSONField(default=list)  # e.g., ["hsn_code", "brand"]
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    def __str__(self):
        return f"{self.user} - {self.company} Columns"

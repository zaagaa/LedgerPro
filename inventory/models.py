from django.db import models
from django.utils import timezone

from company.models import Company

from tax_code.models import Tax_Code

class Floor(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.floor.name} → {self.name}"

class Inventory(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    tax_code=models.ForeignKey(Tax_Code, on_delete=models.SET_NULL, null=True)
    inventory_name=models.CharField(max_length=200)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    shortcode=models.CharField(max_length=10, blank=True, null=True)
    unit_enabled=models.IntegerField(default=0)
    default_price=models.IntegerField(default=None, blank=True, null=True)

    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)

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
    name = models.CharField(max_length=100)
    tax_rate = models.FloatField()
    trigger_amount = models.FloatField()
    inventories = models.ManyToManyField(Inventory, related_name='tax_slabs')

    def __str__(self):
        return self.name

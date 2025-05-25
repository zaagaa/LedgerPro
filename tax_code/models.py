from django.db import models
from django.utils import timezone

from company.models import Company
from BusinessApp.function import int_value


class Tax_Code(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    tax_code=models.IntegerField(default=0, null=True)
    tax_rate=models.IntegerField(default=0,null=True)


    class Meta:
        unique_together = ('company', 'tax_code')

    def __str__(self):
        return self.tax_code

    @property
    def tax_rate_view(self):
        return int_value(self.tax_rate)
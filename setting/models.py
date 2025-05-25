from django.db import models
from django.utils import timezone

from company.models import Company


class Setting(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    setting=models.CharField(max_length=100)
    value=models.CharField(max_length=1000)

    class Meta:
        unique_together = ('company', 'setting')  # Ensures the combination of company and setting is unique
        constraints = [
            models.UniqueConstraint(fields=['company', 'setting'], name='unique_company_setting', condition=models.Q(company__isnull=False))
        ]

    def __str__(self):
        return self.setting

class Master_Setting(models.Model):
    setting=models.CharField(max_length=50, unique=True)
    value=models.CharField(max_length=100)



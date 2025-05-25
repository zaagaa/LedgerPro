

from django.db import models

from company.models import Company
from datetime import *
from django.utils import timezone



class Attribute(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    attribute_name=models.CharField(max_length=100)


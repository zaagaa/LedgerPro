from email.policy import default

from django.db import models
from django.contrib.auth.models import AbstractUser

from company.models import Company
from datetime import *
from django.utils import timezone

from pos.models import Print_Template

from django.contrib.postgres.fields import ArrayField

from django.db.models import JSONField

class User(AbstractUser):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    position_choice=(
        (0, 'Super Admin'),
        (2, 'Billing'),
        (4, 'Purchase Entry'),
        (3, 'Customer Care'),
        (1, 'Administrator'),

    )
    position=models.IntegerField(default=0,null=True, choices=position_choice)
    ip_address=models.CharField(max_length=50, null=True, blank=True)
    raw_password = models.CharField(max_length=50, null=True, blank=True)
    dark_mode = models.IntegerField(default=0, null=True, blank=True)
    pos_template = models.ForeignKey(Print_Template, null=True, blank=True, on_delete=models.SET_NULL)
    # hidden_fields = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    hidden_fields = JSONField(default=list, blank=True)  # ✅ SQLite-safe list
    input_widths = JSONField(default=dict, blank=True)  # New: stores {field_id: width}
    pos_statement_restriction = models.BooleanField(default=False)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    local_ip_address = models.GenericIPAddressField(null=True, blank=True)
    pc_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.method} - {self.path} at {self.timestamp}"
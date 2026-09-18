import os
import sys
import django
from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Q

# ===============================
# DJANGO SETUP (FIRST!)
# ===============================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

# ===============================
# IMPORTS AFTER SETUP
# ===============================

from customer.models import Customer

customers = Customer.objects.exclude(
    mobile__regex=r'^[6-9][0-9]{9}$'
)

print(f"Invalid Indian mobile numbers: {customers.count()}")

for c in customers:
    print(c.id, c.customer_name, c.mobile, c.point)
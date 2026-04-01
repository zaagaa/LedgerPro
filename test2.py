import os
import sys
import django
from datetime import timedelta
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

for c in Customer.objects.all():
    if c.mobile:
        m = str(c.mobile)
        if len(m) != 10:
            print(f"Deleting Customer ID {c.id} Mobile {m}")
            # c.delete()
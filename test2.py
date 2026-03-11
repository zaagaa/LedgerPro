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


from django.db.models import Count

duplicates = Customer.objects.values('mobile').annotate(
    count=Count('mobile')
).filter(count__gt=1)

for item in duplicates:
    print(item['mobile'], item['count'])
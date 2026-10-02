import os
import django



# ===============================
# DJANGO SETUP (FIRST!)
# ===============================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

# ===============================
# IMPORTS AFTER SETUP
# ===============================


from automation.models import Stock_Order_Brand_Setting, Stock_Order_Setting,Stock_Order_WhatsApp_Log
from purchase.models import Stock_Attribute, Stock

import requests
from collections import defaultdict
from math import ceil
from django.utils import timezone
from datetime import timedelta

from scheduler.views import create_auto_order_whatsapp_messages







create_auto_order_whatsapp_messages()


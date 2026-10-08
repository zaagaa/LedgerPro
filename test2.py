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

from scheduler.views import create_auto_order_whatsapp_messages, send_aisensy_whatsapp_message

msg="""Purchase Order

Supplier: NAVEEN COTTON MILL (MANIRAJ)

Order Items:
WHITE SHIRT | SIZE: 36 CM | STYLE: WINNER | TYPE: FULL: 5 boxes      WHITE SHIRT | SIZE: 36 CM | STYLE: WINNER | TYPE: HALF: 5 boxes      WHITE SHIRT | SIZE: 44 CM | STYLE: WINNER | TYPE: FULL: 10 boxes      WHITE SHIRT | SIZE: 44 CM | STYLE: WINNER | TYPE: HALF: 5 boxes 

Total Order Qty: 25 boxes

Please confirm availability and delivery."""

import requests

url = "https://apis.aisensy.com/project-apis/v1/project/6abc95d8af3b98d97e2825e1/messages"

payload = {
    "to": "919585006369",
    "type": "text",
    "recipient_type": "individual",
    "text": { "body": msg },
    "template": { "name": "purchaseorder", "language": {"code": "English"} }
}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-AiSensy-Project-API-Pwd": "215d4f4a4deed449ec110"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())


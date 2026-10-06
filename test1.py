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

import requests

url = "https://apis.aisensy.com/project-apis/v1/project/6abc95d8af3b98d97e2825e1/messages"

payload = {
    "to": "919585006369",
    "type": "text",
    "recipient_type": "individual",
    "text": { "body": "sample query from user?" }
}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-AiSensy-Project-API-Pwd": "1c13e4882fb3756f746f0"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

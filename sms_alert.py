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
from customer.views import send_sms_async,send_sms_to_customer
from setting.views import get_setting

# ===============================
# CONFIG
# ===============================
INACTIVE_DAYS = get_setting("sms_template_id_sms_alert_day")

if not INACTIVE_DAYS or not str(INACTIVE_DAYS).isdigit():
    print("❌ Invalid INACTIVE_DAYS setting. Exiting.")
    sys.exit(0)

INACTIVE_DAYS = int(INACTIVE_DAYS)



# ===============================
# LOGIC
# ===============================
today = timezone.now().date()
threshold_date = today - timedelta(days=INACTIVE_DAYS)

customers = Customer.objects.filter(
    is_active=True,
    point__gt=0,                     # ✅ point above 0
    last_visit__isnull=False,
    last_visit__lte=threshold_date
).filter(
    Q(sms_alert__isnull=True) |
    Q(sms_alert__lte=threshold_date)
)

print(f"📨 Total customers to send SMS: {customers.count()}")
print("-" * 50)

# 🔎 TEST SINGLE NUMBER
customers = Customer.objects.filter(
    mobile="9585006369",
    is_active=True
)

for customer in customers:
    print(
        f"SMS SENT → {customer.customer_name} | "
        f"Last Visit: {customer.last_visit} | "
        f"Previous SMS: {customer.sms_alert}"
    )

    # ===============================
    # SEND SMS
    # ===============================
    template_id = get_setting("sms_template_id_sms_alert")
    template_msg = get_setting("sms_template_content_sms_alert")

    point = f"{customer.point:.2f}"

    content = template_msg.format(
        customer_name=customer.customer_name,
        customer_mobile=customer.mobile,
        customer_point=point
    )

    print(content)
    print(template_id)

    # send_sms_async(customer.mobile, content, template_id)
    result=send_sms_to_customer(customer.mobile, content, template_id)

    print(result,"result")

    # ===============================
    # UPDATE ALERT DATE
    # ===============================
    customer.sms_alert = today
    customer.save(update_fields=["sms_alert"])

    # break

print("-" * 50)
print("✅ SMS process completed successfully")

import threading
import time
import requests
import socket
from invoice.models import Invoice
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()

def get_local_ip():
    """Get the current machine's local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google Public DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"[IP Error] Could not determine local IP: {e}")
        return None

def send_sales_report():
    url = "https://www.zaagaa.in.net/web2/api.php"

    local_ip = get_local_ip()
    print(f"[Local IP] Detected: {local_ip}")

    # ✅ Only proceed if IP is 192.168.1.37
    if local_ip != "192.168.1.37":
        print("[Info] Local IP is not 192.168.1.37, skipping sales report sending...")
        return

    while True:
        try:
            today = now().date()

            # Fetch sales grouped by user_id
            user_sales = (
                Invoice.objects.filter(invoice_date__date=today)
                .values('user_id')
                .annotate(total_sales=Sum('total_amount'))
            )

            report_data = []

            for entry in user_sales:
                user_id = entry['user_id']
                user = User.objects.filter(id=user_id).first()

                if user:  # If user exists
                    report_data.append({
                        "user_id": user_id,
                        "username": user.username,
                        "total_sales": float(entry['total_sales']),
                        "date": today.strftime("%Y-%m-%d"),
                    })

            print("[Sending Report]:", report_data)

            if report_data:  # ✅ Only send if there is some data
                response = requests.post(url, json=report_data, timeout=10)
                print(f"[Sales Report] Sent! Status: {response.status_code}, Response: {response.text}")
            else:
                print("[Info] No sales data to send.")

        except Exception as e:
            print(f"[Sales Report] Error: {e}")

        time.sleep(5*60)  # 30 seconds for testing; change to 5*60 in production

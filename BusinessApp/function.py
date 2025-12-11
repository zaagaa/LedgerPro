import requests
from django.http import JsonResponse

from setting.models import Setting, Master_Setting
from sync.models import Deleted_Record
from django.db import connection

def invoice_type():
    db_settings = connection.settings_dict
    db_name = db_settings.get('NAME', '')
    db_host = db_settings.get('HOST', '')

    # Check if Railway (online)
    if 'railway' in db_name or 'railway' in db_host or 'proxy.rlwy.net' in db_host:
        return 2  # online
    return 1  # offline


def decimal_value(number):
    return float('%.2f' % (number))


def int_value(value):
    value=float(value)
    if value==int(value):
        return int(value)
    else:
        return decimal_value(value)


def proxy_print(request, receipt_text):


    print(receipt_text,"VICKYYYYYYYYYYYY")
    try:
        #  Accept printer name from query param or default
        printer_name = request.user.printer_name

        payload = {
            "print_text": receipt_text,
            "printer_name": printer_name
        }

        print(payload)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            agent_ip = x_forwarded_for.split(',')[0]
        else:
            agent_ip = request.META.get('REMOTE_ADDR')

        print(agent_ip,"agent_ip")


        try:
            response = requests.post(f"http://{agent_ip}:9999", json=payload, timeout=5)
            status = response.status_code
            message = response.text.strip()

            if status == 200:
                return JsonResponse({"status": "success", "message": message})
            else:
                return JsonResponse({"status": "error", "message": message or "Print failed"}, status=500)

        except:
            pass

    except:
        pass
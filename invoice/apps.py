from django.apps import AppConfig
import threading
import os

class InvoiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invoice'  # App name

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':  # Important: prevents duplicate thread
            return

        from .background import send_sales_report
        thread = threading.Thread(target=send_sales_report)
        thread.daemon = True
        thread.start()

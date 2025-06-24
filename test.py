
import os
import django
#
# # Set Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
# django.setup()
#
# from datetime import timedelta
# from invoice.models import Invoice
#
# updated = 0
#
# # Process newest invoices first
# for inv in Invoice.objects.order_by('-invoice_date'):
#     dt = inv.invoice_date
#     if dt:
#         t = dt.time()
#
#         # Skip if time is exactly 05:30:00
#         if t.hour == 5 and t.minute == 30 and t.second == 0:
#             continue
#
#         # Subtract 5.5 hours
#         inv.invoice_date = dt - timedelta(hours=5, minutes=30)
#         print(inv.invoice_date, inv.id)
#         inv.save()
#         updated += 1
#
#
# print(f"{updated} invoice timestamps updated by subtracting 5.5 hours.")

import os
import django

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

from customer.models import Customer
from invoice.models import Point_Entry

for customer in Customer.objects.all():
    last_entry = (
        Point_Entry.objects
        .filter(customer=customer)
        .order_by("-entry_date")
        .first()
    )

    if last_entry:
        visit_date = last_entry.entry_date.date()
        customer.last_visit = visit_date
        customer.save(update_fields=["last_visit"])

        print(customer.customer_name, "→", visit_date)

print("✅ Last visit update completed")

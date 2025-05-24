import os
import django

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

from invoice.models import Invoice
from django.db import transaction
import re

def parse_discount(discount_str):
    if not discount_str:
        return ("flat", 0)
    discount_str = discount_str.strip()
    try:
        if discount_str.endswith('%'):
            return ("percent", float(discount_str.rstrip('%')))
        else:
            return ("flat", float(re.sub(r'[^\d.]', '', discount_str)))
    except ValueError:
        return ("flat", 0)

batch_size = 1000
offset = 0

while True:
    with transaction.atomic():
        invoices = Invoice.objects.prefetch_related('sale_set').order_by('-id')[offset:offset+batch_size]
        if not invoices:
            break

        print(f"🔁 Processing invoices [{offset + 1} – {offset + len(invoices)}]")

        for invoice in invoices:
            sales = invoice.sale_set.all()
            if not sales:
                continue

            total_sale_price = sum(sale.sale_price for sale in sales)
            inv_disc_type, inv_disc_value = parse_discount(invoice.discount)

            updated = False

            for sale in sales:
                base_price = sale.sale_price

                # STEP 1: Apply sale-level discount
                sale_disc_type, sale_disc_value = parse_discount(sale.discount)
                if sale_disc_type == "percent":
                    base_price = base_price * (1 - sale_disc_value / 100)
                elif sale_disc_type == "flat":
                    base_price = base_price - sale_disc_value

                # STEP 2: Apply invoice-level discount
                if inv_disc_type == "percent":
                    base_price = base_price * (1 - inv_disc_value / 100)
                elif inv_disc_type == "flat" and total_sale_price > 0:
                    proportional_disc = (sale.sale_price / total_sale_price) * inv_disc_value
                    base_price = base_price - proportional_disc

                sale.actual_sale_price = round(base_price, 2)
                sale.save(update_fields=['actual_sale_price'])
                updated = True

            if updated:
                print(f"✅ Updated Invoice ID: {invoice.id} with {len(sales)} sale(s)")

    offset += batch_size

print("🏁 All invoices processed successfully.")

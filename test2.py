import os
import django
import time
from django.apps import apps
from django.db import connection
from psycopg2 import sql



# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from customer.models import Customer
from invoice.models import Point_Entry




from escpos.printer import Win32Raw

try:
    printer = Win32Raw("RP3160 GOLD(U) 1")
    printer.text("Test Print\n")
    printer.cut()
    printer.close()
    print("Print successful")
except Exception as e:
    print(f"Printer error: {e}")


# def current_unix_ms():
#     return int(time.time() * 1000)
#
# unix_time = current_unix_ms()
# print(f"📌 Fixed Unix Time: {unix_time}\n")
#
# excluded_apps = ['admin', 'auth', 'contenttypes', 'sessions']
# sync_fields = ['sync_online', 'sync_offline']
# total_tables = 0
#
# with connection.cursor() as cursor:
#     for model in apps.get_models():
#         model_name = model._meta.label
#         table_name = model._meta.db_table
#
#         if model._meta.app_label in excluded_apps:
#             continue
#
#         field_names = [f.name for f in model._meta.fields]
#         if not all(field in field_names for field in sync_fields):
#             continue
#
#         print(f"🔧 Resetting columns in: {table_name} ({model_name})")
#         total_tables += 1
#
#         for field in sync_fields:
#             try:
#                 cursor.execute(sql.SQL(
#                     "ALTER TABLE {} DROP COLUMN IF EXISTS {}"
#                 ).format(
#                     sql.Identifier(table_name),
#                     sql.Identifier(field)
#                 ))
#                 print(f"   ❌ Dropped column: {field}")
#             except Exception as e:
#                 print(f"   ⚠️ Failed to drop {field}: {e}")
#
#         for field in sync_fields:
#             try:
#                 cursor.execute(sql.SQL(
#                     "ALTER TABLE {} ADD COLUMN {} BIGINT DEFAULT %s NOT NULL"
#                 ).format(
#                     sql.Identifier(table_name),
#                     sql.Identifier(field)
#                 ), [unix_time])
#                 print(f"   ➕ Recreated column: {field} = {unix_time}")
#             except Exception as e:
#                 print(f"   ⚠️ Failed to create {field}: {e}")
#
# print(f"\n🎯 Done! Total tables updated: {total_tables}")
#
# Purchase.objects.filter(stock_only=None).update(stock_only=0)
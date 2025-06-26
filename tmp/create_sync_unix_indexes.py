import os
import django
from django.apps import apps
from django.db import connections
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

def has_column(model, column_name, db_alias='default'):
    table = model._meta.db_table
    with connections[db_alias].cursor() as cursor:
        cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = %s
        """, [table])
        return column_name in [row[0] for row in cursor.fetchall()]

def index_exists(table, index_name, db_alias='default'):
    with connections[db_alias].cursor() as cursor:
        cursor.execute("""
            SELECT indexname FROM pg_indexes
            WHERE tablename = %s AND indexname = %s
        """, [table, index_name])
        return cursor.fetchone() is not None

def create_index_if_needed(model):
    db_alias = 'default'
    table = model._meta.db_table
    if not has_column(model, 'sync_unix', db_alias):
        return

    index_name = f"idx_{model._meta.app_label}_{model._meta.model_name}_sync_unix"
    if index_exists(table, index_name, db_alias):
        print(f" Index already exists: {index_name}")
        return

    with connections[db_alias].cursor() as cursor:
        try:
            cursor.execute(f'CREATE INDEX {index_name} ON "{table}" (sync_unix);')
            print(f"➕ Created index: {index_name} on table: {table}")
        except Exception as e:
            print(f"❌ Failed to create index on {table}: {e}")

def main():
    print("🔍 Scanning models for sync_unix indexing...\n")
    for model in apps.get_models():
        if 'sync_unix' in [f.name for f in model._meta.fields]:
            create_index_if_needed(model)
    print("\n Indexing complete.")

if __name__ == "__main__":
    main()

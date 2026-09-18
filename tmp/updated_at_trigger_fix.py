import os
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

def fetch_triggers_with_updated_at():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tg.tgname, c.relname AS tablename
            FROM pg_trigger tg
            JOIN pg_class c ON tg.tgrelid = c.oid
            JOIN pg_proc p ON tg.tgfoid = p.oid
            WHERE NOT tg.tgisinternal
              AND (
                  p.prosrc ILIKE '%updated_at%'
                  OR tg.tgname ILIKE '%updated_at%'
              )
        """)
        return cursor.fetchall()

def drop_trigger(trigger_name, table_name):
    with connection.cursor() as cursor:
        try:
            print(f"🧹 Dropping trigger '{trigger_name}' on table '{table_name}'...")
            cursor.execute(f'DROP TRIGGER IF EXISTS "{trigger_name}" ON "{table_name}" CASCADE;')
            print(f" Dropped trigger: {trigger_name} on {table_name}")
        except Exception as e:
            print(f"❌ Failed to drop trigger {trigger_name} on {table_name}: {e}")

def drop_unused_functions_with_updated_at():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT proname
            FROM pg_proc
            WHERE prosrc ILIKE '%updated_at%'
              AND proname NOT IN (
                  SELECT p.proname
                  FROM pg_trigger t
                  JOIN pg_proc p ON t.tgfoid = p.oid
              )
        """)
        functions = cursor.fetchall()
        for (func,) in functions:
            try:
                print(f"🧹 Dropping unused function '{func}'...")
                cursor.execute(f'DROP FUNCTION IF EXISTS {func}() CASCADE;')
                print(f" Dropped function: {func}()")
            except Exception as e:
                print(f"❌ Failed to drop function {func}(): {e}")

def run():
    print("🔍 Scanning for triggers referencing 'updated_at'...")
    triggers = fetch_triggers_with_updated_at()
    for trigger_name, table_name in triggers:
        drop_trigger(trigger_name, table_name)

    print("🔍 Scanning for unused functions referencing 'updated_at'...")
    drop_unused_functions_with_updated_at()

if __name__ == "__main__":
    run()

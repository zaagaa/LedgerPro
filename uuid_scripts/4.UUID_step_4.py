import psycopg2

import json

# ==== LOAD DB CONFIG ====
with open("../db_config.json", "r") as f:
    config = json.load(f)

DB_NAME = config["NAME"]
DB_USER = config["USER"]
DB_PASS = config["PASSWORD"]
DB_HOST = config["HOST"]
DB_PORT = config["PORT"]

# ==== CONNECT ====
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()
print("✅ Connected to database.")

# ==== GET TABLES ====
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
all_tables = [row[0] for row in cur.fetchall()]

# ==== FILTER CUSTOM TABLES ====
def is_custom(table):
    return not (
        table.startswith("auth_") or
        table.startswith("django_") or
        table.startswith("admin_") or
        table.startswith("sessions_")
        # table.startswith("authentication_")
    )

custom_tables = [t for t in all_tables if is_custom(t)]
print(f"🎯 Custom tables: {custom_tables}")

# ==== SCAN TABLES FOR _uuid COLUMNS ====
for table in custom_tables:


    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = %s AND column_name LIKE %s;
    """, (table, r'%\_uuid'))  # ✅ No warning

    uuid_columns = [row[0] for row in cur.fetchall()]

    if uuid_columns:
        print(f"\n🔧 Table: {table}")
        for uuid_col in uuid_columns:
            new_name = uuid_col.replace('_uuid', '_id')
            try:
                print(f"  🔁 Renaming column {uuid_col} → {new_name}")
                cur.execute(f"ALTER TABLE {table} RENAME COLUMN {uuid_col} TO {new_name};")
                conn.commit()
            except Exception as e:
                print(f"  ❌ Failed to rename {uuid_col} in {table}: {e}")
                conn.rollback()
    else:
        print(f"⏭️ No _uuid columns in {table}")

cur.close()
conn.close()
print("\n✅ All _uuid columns renamed to _id.")

import psycopg2
import json

# ==== LOAD DB CONFIG ====
with open("db_config.json", "r") as f:
    config = json.load(f)

conn = psycopg2.connect(
    dbname=config["NAME"],
    user=config["USER"],
    password=config["PASSWORD"],
    host=config["HOST"],
    port=config["PORT"]
)
cur = conn.cursor()
print("✅ Connected to database.")

# ==== GET CUSTOM TABLES ====
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
all_tables = [r[0] for r in cur.fetchall()]

def is_custom(table):
    return not (
        table.startswith("auth_") or
        table.startswith("django_") or
        table.startswith("admin_") or
        table.startswith("sessions_") or
        table.startswith("authentication_")
    )

custom_tables = [t for t in all_tables if is_custom(t)]
print("📋 Custom tables found:", custom_tables)

# ==== DROP old_id & uuid / ADD sync, created_at, updated_at, is_deleted ====
# tracking_fields = {
#     "sync": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
#     "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
#     "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
#     "is_deleted": "BOOLEAN DEFAULT FALSE"
# }

tracking_fields = {
    "sync": "TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP",
    "created_at": "TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP",
    "is_deleted": "BOOLEAN DEFAULT FALSE"
}

for table in custom_tables:
    print(f"\n🛠 Processing: {table}")

    # Drop old_id and uuid
    for col in ['old_id', 'uuid']:
        cur.execute("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name = %s AND column_name = %s;
        """, (table, col))
        if cur.fetchone():
            try:
                print(f"❌ Dropping column: {col}")
                cur.execute(f"ALTER TABLE {table} DROP COLUMN {col};")
                conn.commit()
            except Exception as e:
                print(f"⚠️ Failed to drop {col} from {table}: {e}")
                conn.rollback()
        else:
            print(f"⏭️ Column {col} not found")

    # Add new tracking fields
    for col, datatype in tracking_fields.items():
        cur.execute("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name = %s AND column_name = %s;
        """, (table, col))
        if not cur.fetchone():
            try:
                print(f"➕ Adding column: {col}")
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {datatype};")
                conn.commit()
            except Exception as e:
                print(f"⚠️ Failed to add {col} to {table}: {e}")
                conn.rollback()
        else:
            print(f"✅ Column {col} already exists")

cur.close()
conn.close()
print("\n✅ All updates completed.")

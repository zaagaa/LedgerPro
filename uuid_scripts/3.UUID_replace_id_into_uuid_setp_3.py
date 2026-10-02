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
        table.startswith("sessions_") or
        table.startswith("authentication_")
    )

custom_tables = [t for t in all_tables if is_custom(t)]
print(f"🎯 Custom tables: {custom_tables}")

# ==== PROCESS EACH TABLE ====
for table in custom_tables:
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = %s AND column_name IN ('id', 'uuid');
    """, (table,))
    columns = [r[0] for r in cur.fetchall()]

    if 'id' in columns and 'uuid' in columns:
        print(f"\n🔄 Processing table: {table}")

        try:
            # Rename id to old_id
            print(f"  ➡️ Renaming id → old_id")
            cur.execute(f"ALTER TABLE {table} RENAME COLUMN id TO old_id;")
            conn.commit()
        except Exception as e:
            print(f"  ⚠️ Failed to rename id on {table}: {e}")
            conn.rollback()
            continue

        try:
            # Add new UUID id column
            print(f"  ➕ Creating new id column (UUID)")
            cur.execute(f"ALTER TABLE {table} ADD COLUMN id UUID;")
            conn.commit()
        except Exception as e:
            print(f"  ⚠️ Failed to add id column on {table}: {e}")
            conn.rollback()
            continue

        try:
            # Copy uuid values into new id
            print(f"  📝 Copying uuid → id")
            cur.execute(f"UPDATE {table} SET id = uuid;")
            conn.commit()
        except Exception as e:
            print(f"  ⚠️ Failed to copy uuid to id on {table}: {e}")
            conn.rollback()
            continue

        try:
            # Find and drop old primary key
            cur.execute("""
                SELECT constraint_name FROM information_schema.table_constraints
                WHERE table_name = %s AND constraint_type = 'PRIMARY KEY';
            """, (table,))
            pk_result = cur.fetchone()
            if pk_result:
                constraint_name = pk_result[0]
                print(f"  ❌ Dropping old PRIMARY KEY: {constraint_name}")
                cur.execute(f"ALTER TABLE {table} DROP CONSTRAINT {constraint_name};")
                conn.commit()
        except Exception as e:
            print(f"  ⚠️ Failed to drop old PRIMARY KEY on {table}: {e}")
            conn.rollback()

        try:
            # Set new primary key
            print(f"  🔐 Setting id as PRIMARY KEY")
            cur.execute(f"ALTER TABLE {table} ADD PRIMARY KEY (id);")
            conn.commit()
        except Exception as e:
            print(f"  ❌ Failed to set PRIMARY KEY on {table}: {e}")
            conn.rollback()
            continue

    else:
        print(f"⏭️ Skipping {table} (missing both id and uuid columns)")

# ==== CLOSE ====
cur.close()
conn.close()
print("\n✅ ID replacement complete.")

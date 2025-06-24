import psycopg2
from psycopg2.extras import DictCursor


import json

# ==== LOAD DB CONFIG ====
with open("../db_config.json", "r") as f:
    config = json.load(f)

DB_NAME = config["NAME"]
DB_USER = config["USER"]
DB_PASS = config["PASSWORD"]
DB_HOST = config["HOST"]
DB_PORT = config["PORT"]


# ==== DB CONFIG ====
# ==== CONNECT ====
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor(cursor_factory=DictCursor)
print("✅ Connected to database.")

# ==== GET FK RELATIONSHIPS ====
cur.execute("""
SELECT
    tc.table_name AS child_table,
    kcu.column_name AS child_column,
    ccu.table_name AS parent_table,
    ccu.column_name AS parent_column
FROM
    information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
WHERE
    tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
    AND kcu.column_name LIKE '%_id'
ORDER BY child_table;
""")
fks = cur.fetchall()

print(f"🔍 Found {len(fks)} foreign key mappings.\n")

for fk in fks:
    child_table = fk['child_table']
    child_column = fk['child_column']
    parent_table = fk['parent_table']
    parent_column = fk['parent_column']
    new_column = child_column.replace("_id", "_uuid")

    try:
        # Skip if parent table doesn't have uuid column
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = %s AND column_name = 'uuid'
            );
        """, (parent_table,))
        if not cur.fetchone()[0]:
            print(f"⚠️ Skipped: {child_table}.{child_column} → Parent '{parent_table}' missing uuid")
            continue

        # Add UUID column to child table if not exists
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = %s AND column_name = %s
            );
        """, (child_table, new_column))
        if not cur.fetchone()[0]:
            print(f"➕ Adding column: {child_table}.{new_column}")
            cur.execute(f"""ALTER TABLE {child_table} ADD COLUMN {new_column} UUID;""")

        # Update new column with UUID values from parent
        print(f"🔁 Mapping UUID: {child_table}.{new_column} ← {parent_table}.uuid")
        cur.execute(f"""
            UPDATE {child_table} AS child
            SET {new_column} = parent.uuid
            FROM {parent_table} AS parent
            WHERE child.{child_column} = parent.{parent_column};
        """)

        # Drop old _id column
        print(f"❌ Dropping column: {child_table}.{child_column}")
        cur.execute(f"""ALTER TABLE {child_table} DROP COLUMN {child_column} CASCADE;""")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"❌ Error processing {child_table}.{child_column}: {e}")

print("\n✅ UUID migration completed.")
cur.close()
conn.close()

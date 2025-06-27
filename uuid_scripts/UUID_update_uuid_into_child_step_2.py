import psycopg2

import json

# ==== LOAD DB CONFIG ====
with open("db_config.json", "r") as f:
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

cur = conn.cursor()
print("✅ Connected to database.")

# ==== GET FK RELATIONSHIPS ====
cur.execute("""
SELECT
    tc.table_name AS child_table,
    kcu.column_name AS child_column,
    ccu.table_name AS parent_table,
    ccu.column_name AS parent_column
FROM
    information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name AND tc.table_name = kcu.table_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE
    constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
    AND kcu.column_name LIKE '%_id'
ORDER BY child_table;
""")
fks = cur.fetchall()

# ==== PROCESS FK MAPPINGS ====
for child_table, child_column, parent_table, parent_column in fks:
    new_column = child_column.replace("_id", "_uuid")

    # Check parent has uuid
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = %s AND column_name = 'uuid';
    """, (parent_table,))
    if not cur.fetchone():
        print(f"⚠️ Skipped: {child_table}.{child_column} → Parent table '{parent_table}' missing uuid")
        continue

    # Add new _uuid column if not exists
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s;
    """, (child_table, new_column))
    if not cur.fetchone():
        print(f"➕ Adding {new_column} to {child_table}")
        cur.execute(f"""ALTER TABLE {child_table} ADD COLUMN {new_column} UUID;""")
        conn.commit()

    # Copy uuid values
    print(f"🔁 Updating {child_table}.{new_column} from {parent_table}.uuid")
    cur.execute(f"""
        UPDATE {child_table} AS child
        SET {new_column} = parent.uuid
        FROM {parent_table} AS parent
        WHERE child.{child_column} = parent.{parent_column};
    """)
    conn.commit()

    # Drop old column
    print(f"❌ Dropping {child_column} from {child_table}")
    cur.execute(f"""ALTER TABLE {child_table} DROP COLUMN {child_column} CASCADE;""")
    conn.commit()

print("✅ All valid foreign keys converted to UUID.")
cur.close()
conn.close()

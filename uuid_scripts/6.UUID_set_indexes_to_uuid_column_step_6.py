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

# ==== FETCH UUID COLUMNS ====
cur.execute("""
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND data_type = 'uuid';
""")

uuid_columns = cur.fetchall()
print(f"🔍 Found {len(uuid_columns)} UUID columns.")

# ==== CREATE INDEX IF NOT EXISTS ====
for table_name, column_name in uuid_columns:
    index_name = f"idx_{table_name}_{column_name}"
    print(f"➡️  Checking index for: {table_name}.{column_name}")

    cur.execute("""
        SELECT 1 FROM pg_indexes
        WHERE tablename = %s AND indexname = %s;
    """, (table_name, index_name))

    if cur.fetchone():
        print(f"✅ Index already exists: {index_name}")
    else:
        cur.execute(f"""
            CREATE INDEX {index_name} ON {table_name} ({column_name});
        """)
        print(f"✅ Created index: {index_name}")

# ==== COMMIT & CLOSE ====
conn.commit()
cur.close()
conn.close()
print("🎉 All UUID indexes are ensured.")

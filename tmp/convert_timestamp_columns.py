import psycopg2
import psycopg2.extras

# Railway PostgreSQL URL
DATABASE_URL = "postgresql://postgres:NMHhPdMGJYCfxMGkTiOJxxyiTZsRWCVQ@nozomi.proxy.rlwy.net:23414/railway"

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Step 1: Get all timestamp columns without time zone
query = """
SELECT table_schema, table_name, column_name
FROM information_schema.columns
WHERE data_type = 'timestamp without time zone'
AND table_schema = 'public';
"""

cursor.execute(query)
rows = cursor.fetchall()

print(f"🧩 Found {len(rows)} timestamp columns without timezone.")

# Step 2: Convert each one to TIMESTAMP WITH TIME ZONE
for row in rows:
    schema = row["table_schema"]
    table = row["table_name"]
    column = row["column_name"]
    alter_sql = f"""
    ALTER TABLE "{schema}"."{table}"
    ALTER COLUMN "{column}" TYPE TIMESTAMP WITH TIME ZONE;
    """
    try:
        print(f"🔧 Updating {table}.{column} → TIMESTAMP WITH TIME ZONE")
        cursor.execute(alter_sql)
    except Exception as e:
        print(f"❌ Failed to update {table}.{column}: {e}")
        conn.rollback()
    else:
        conn.commit()
        print(f" Success: {table}.{column}")

cursor.close()
conn.close()
print("\n🎉 All eligible timestamp columns updated.")

import psycopg2
import uuid
import json

# ==== LOAD DB CONFIG ====
with open("db_config.json", "r") as f:
    config = json.load(f)

DB_NAME = config["NAME"]
DB_USER = config["USER"]
DB_PASS = config["PASSWORD"]
DB_HOST = config["HOST"]
DB_PORT = config["PORT"]
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

# ==== STEP 1: Get all user-defined tables (skip system tables) ====
cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
all_tables = [r[0] for r in cur.fetchall()]

def is_custom_table(table):
    return not (
        table.startswith("auth_") or
        table.startswith("django_") or
        table.startswith("admin_") or
        table.startswith("sessions_") or
        table.startswith("authentication_")
    )

custom_tables = [t for t in all_tables if is_custom_table(t)]
print("📋 Custom tables to process:", custom_tables)

# ==== STEP 2: Add and Fill UUID ====
for table in custom_tables:
    print(f"\n🔧 Processing table: {table}")

    cur.execute("""
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = 'uuid';
    """, (table,))
    has_uuid = cur.fetchone()

    if not has_uuid:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN uuid UUID;")
        print(f"  ➕ Added 'uuid' column")

    cur.execute(f"SELECT COUNT(*) FROM {table} WHERE uuid IS NULL;")
    count = cur.fetchone()[0]
    if count > 0:
        cur.execute(f"SELECT ctid FROM {table} WHERE uuid IS NULL;")
        rows = cur.fetchall()
        for row in rows:
            uid = str(uuid.uuid4())
            cur.execute(f"UPDATE {table} SET uuid = %s WHERE ctid = %s", (uid, row[0]))
        conn.commit()
        print(f"  ✅ Filled {count} UUIDs")
    else:
        print("  ✅ UUIDs already filled")

# ==== STEP 3: Convert PKs and FKs ====
for table in custom_tables:
    print(f"\n🔍 Checking PK for: {table}")

    cur.execute("""
        SELECT a.attname, t.typname
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
        JOIN pg_class c ON c.oid = i.indrelid
        JOIN pg_type t ON a.atttypid = t.oid
        WHERE i.indisprimary AND c.relname = %s;
    """, (table,))
    pk_info = cur.fetchone()
    if not pk_info:
        print("  ⚠ No PK found. Skipping.")
        continue

    pk_col, pk_type = pk_info
    if pk_type != "int4":
        print(f"  ✅ PK is already {pk_type}. Skipping.")
        continue

    print(f"  🎯 Converting PK {table}.{pk_col}")

    # ==== Update referencing foreign keys ====
    cur.execute(f"""
        SELECT conname, conrelid::regclass::text AS child_table,
               a.attname AS fk_col
        FROM pg_constraint
        JOIN pg_attribute a ON a.attrelid = conrelid AND a.attnum = ANY(conkey)
        WHERE confrelid = '{table}'::regclass AND contype = 'f';
    """)
    fk_refs = cur.fetchall()

    for conname, child_table, fk_col in fk_refs:
        print(f"    🔁 Updating FK in {child_table}.{fk_col}")
        cur.execute(f"ALTER TABLE {child_table} ADD COLUMN IF NOT EXISTS {fk_col}_uuid UUID;")
        conn.commit()

        cur.execute(f"""
            UPDATE {child_table} AS c
            SET {fk_col}_uuid = p.uuid
            FROM {table} AS p
            WHERE c.{fk_col} = p.{pk_col};
        """)
        conn.commit()

        cur.execute(f"ALTER TABLE {child_table} DROP CONSTRAINT IF EXISTS {conname};")
        cur.execute(f"ALTER TABLE {child_table} DROP COLUMN {fk_col};")
        cur.execute(f"ALTER TABLE {child_table} RENAME COLUMN {fk_col}_uuid TO {fk_col};")
        conn.commit()

        fk_name = f"{child_table[:30]}_{fk_col[:20]}_fkey"
        cur.execute(f"""
            ALTER TABLE {child_table}
            ADD CONSTRAINT {fk_name}
            FOREIGN KEY ({fk_col})
            REFERENCES {table}(uuid)
            ON DELETE SET NULL;
        """)
        conn.commit()
        print(f"    ✅ FK converted to UUID")

    # ==== Replace Primary Key ====
    print(f"  🔁 Replacing PK {pk_col} with UUID")

    cur.execute(f"""
        DO $$
        DECLARE r RECORD;
        BEGIN
            FOR r IN (
                SELECT conname, conrelid::regclass::text AS tname
                FROM pg_constraint
                WHERE confrelid = '{table}'::regclass AND contype = 'f'
            ) LOOP
                EXECUTE format('ALTER TABLE %I DROP CONSTRAINT %I', r.tname, r.conname);
            END LOOP;
        END $$;
    """)
    conn.commit()

    cur.execute(f"ALTER TABLE {table} DROP CONSTRAINT {table}_pkey;")
    cur.execute(f"ALTER TABLE {table} ALTER COLUMN uuid SET NOT NULL;")
    cur.execute(f"ALTER TABLE {table} ADD PRIMARY KEY (uuid);")
    conn.commit()

    cur.execute(f"ALTER TABLE {table} DROP COLUMN {pk_col};")
    cur.execute(f"ALTER TABLE {table} RENAME COLUMN uuid TO {pk_col};")
    conn.commit()

    print(f"  ✅ PK replaced with UUID in {table}")

# ==== DONE ====
cur.close()
conn.close()
print("\n🎉 UUID conversion completed for ALL CUSTOM TABLES (system tables skipped)!")

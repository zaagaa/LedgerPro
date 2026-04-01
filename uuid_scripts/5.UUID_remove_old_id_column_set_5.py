import psycopg2
import json

# ==== LOAD DB CONFIG ====
with open("../db_config.json", "r") as f:
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

# ==== STEP 0: Setup global sequence and trigger function ====
print("\n⚙️ Setting up global sequence and trigger function...")
try:
    cur.execute("""
        CREATE SEQUENCE IF NOT EXISTS updated_at_seq START 1;

        CREATE OR REPLACE FUNCTION set_ordered_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at := TIMESTAMP '2000-01-01' + (nextval('updated_at_seq') || ' seconds')::interval;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    conn.commit()
    print("✅ Sequence and trigger function created.")
except Exception as e:
    print(f"❌ Failed to setup sequence or trigger function: {e}")
    conn.rollback()

# ==== Tracking Fields to Add ====
tracking_fields = {
    "sync": "TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP",
    "created_at": "TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP",
    "is_deleted": "BOOLEAN DEFAULT FALSE"
}

# ==== Loop Tables ====
for table in custom_tables:
    print(f"\n🛠 Processing: {table}")

    # Step 1: Add tracking fields
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

    # Step 2: Backfill created_at and updated_at using old_id or id
    used_col = None
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = 'old_id';
    """, (table,))
    if cur.fetchone():
        used_col = 'old_id'
    else:
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s AND column_name = 'id';
        """, (table,))
        if cur.fetchone():
            used_col = 'id'

    if used_col:
        print(f"⏪ Backfilling created_at and updated_at using: {used_col}")
        try:
            cur.execute(f"""
                WITH ordered AS (
                    SELECT {used_col}, ROW_NUMBER() OVER (ORDER BY {used_col}) AS rn
                    FROM {table}
                )
                UPDATE {table}
                SET created_at = TIMESTAMP '2000-01-01' + (ordered.rn || ' seconds')::interval,
                    updated_at = TIMESTAMP '2000-01-01' + (ordered.rn || ' seconds')::interval
                FROM ordered
                WHERE {table}.{used_col} = ordered.{used_col};
            """)
            conn.commit()
            print("✅ Backfill completed")
        except Exception as e:
            print(f"⚠️ Backfill failed: {e}")
            conn.rollback()
    else:
        print("⏭️ Skipped backfill (no 'old_id' or 'id' found)")

    # Step 3: Drop old_id and uuid (after backfill)
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

    # Step 4: Attach trigger to set updated_at for future inserts/updates
    try:
        print(f"🔗 Attaching trigger to {table}")
        cur.execute(f"""
            DROP TRIGGER IF EXISTS trg_updated_at_ordered ON {table};
            CREATE TRIGGER trg_updated_at_ordered
            BEFORE INSERT OR UPDATE ON {table}
            FOR EACH ROW
            EXECUTE FUNCTION set_ordered_updated_at();
        """)
        conn.commit()
        print("✅ Trigger attached")
    except Exception as e:
        print(f"⚠️ Failed to attach trigger: {e}")
        conn.rollback()

# ==== DONE ====
cur.close()
conn.close()
print("\n✅ All updates, triggers, and backfills completed.")

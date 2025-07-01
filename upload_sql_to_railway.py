import os
import subprocess
import sys
import psycopg2
import urllib.parse
from django.apps import apps
from django.db import connections, DEFAULT_DB_ALIAS
from dotenv import load_dotenv
import django

# === Setup Django environment ===
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()


def get_online_db_url_from_setting():
    Setting = apps.get_model("setting", "Setting")
    try:
        setting_obj = Setting.objects.using(DEFAULT_DB_ALIAS).filter(setting="online_database_url").last()
        return setting_obj.value if setting_obj else None
    except Exception as e:
        print(f"❌ Failed to fetch 'online_database_url' from Setting model: {e}")
        return None


# === Get online DATABASE_URL ===
DATABASE_URL = get_online_db_url_from_setting()
DATABASE_URL = "postgresql://postgres:NMHhPdMGJYCfxMGkTiOJxxyiTZsRWCVQ@nozomi.proxy.rlwy.net:23414/railway"
if not DATABASE_URL:
    print("❌ No DATABASE_URL found. Exiting.")
    sys.exit(1)

# === Path to SQL file ===
sql_file = r"D:\backup.sql"

# === Path to psql.exe ===
PSQL_PATH = r"C:\Program Files\PostgreSQL\17\bin\psql.exe"

# === Validation ===
if not os.path.exists(sql_file):
    raise FileNotFoundError(f"❌ SQL file not found: {sql_file}")
if not os.path.exists(PSQL_PATH):
    raise FileNotFoundError(f"❌ psql.exe not found at: {PSQL_PATH}")

# === Parse DATABASE_URL ===
parsed = urllib.parse.urlparse(DATABASE_URL)
PG_USER = parsed.username
PG_PASSWORD = parsed.password
PG_HOST = parsed.hostname
PG_PORT = str(parsed.port)
PG_DATABASE = parsed.path.lstrip("/")

os.environ["PGPASSWORD"] = PG_PASSWORD

# === Terminate existing connections ===.
print("🔌 Attempting to terminate existing connections...")

try:
    conn = psycopg2.connect(dbname="postgres", user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{PG_DATABASE}' AND pid <> pg_backend_pid();
    """)
    cur.close()
    conn.close()
    print("✅ Existing connections terminated.")
except Exception as e:
    print(f"⚠️ Could not terminate existing connections: {e}")

# === Drop, recreate DB and set timezone ===
print("🧹 Dropping, recreating, and configuring database...")

try:
    # Drop database
    subprocess.run(
        [PSQL_PATH, "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT, "-d", "postgres", "-c",
         f"DROP DATABASE IF EXISTS {PG_DATABASE};"],
        check=True
    )

    # Recreate database
    subprocess.run(
        [PSQL_PATH, "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT, "-d", "postgres", "-c",
         f"CREATE DATABASE {PG_DATABASE} WITH OWNER = {PG_USER} ENCODING = 'UTF8';"],
        check=True
    )

    # Set timezone
    subprocess.run(
        [PSQL_PATH, "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT, "-d", "postgres", "-c",
         f"ALTER DATABASE {PG_DATABASE} SET timezone TO 'Asia/Kolkata';"],
        check=True
    )

    print("✅ Database dropped, recreated, and timezone set.")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed during drop/create/set timezone: {e}")
    sys.exit(1)

# === Restore SQL ===
print(f"📦 Restoring SQL from: {sql_file}")

try:
    subprocess.run(
        [PSQL_PATH, "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT, "-d", PG_DATABASE, "-f", sql_file],
        check=True
    )
    print("✅ Restore completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"❌ Restore failed: {e}")
    sys.exit(1)

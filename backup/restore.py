import os
import subprocess
import sys
import psycopg2

# === Set the SQL file path you want to restore ===
sql_file = r"E:\backup.sql"

# === Full path to psql.exe (update if installed elsewhere) ===
PSQL_PATH = r"C:\Program Files\PostgreSQL\17\bin\psql.exe"

if not os.path.exists(sql_file):
    raise FileNotFoundError(f"❌ SQL file not found: {sql_file}")

# === Dynamically get Django project name ===
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

for item in os.listdir(project_root):
    settings_path = os.path.join(project_root, item, "settings.py")
    if os.path.isdir(os.path.join(project_root, item)) and os.path.isfile(settings_path):
        django_project_name = item
        break
else:
    raise Exception("❌ Could not find Django settings.py")

sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{django_project_name}.settings")

import django
django.setup()

from django.conf import settings

# === Extract DB credentials from Django settings ===
db_settings = settings.DATABASES['default']
PG_USER = db_settings['USER']
PG_PASSWORD = db_settings['PASSWORD']
PG_DATABASE = db_settings['NAME']
PG_PORT = str(db_settings['PORT'])  # Ensure it's a string
PG_HOST = db_settings['HOST']

os.environ["PGPASSWORD"] = PG_PASSWORD

if not os.path.exists(PSQL_PATH):
    raise FileNotFoundError(f"❌ psql.exe not found at: {PSQL_PATH}")

# === Force disconnect all connections to the database ===
print("🔌 Terminating existing connections to the database...")

try:
    conn = psycopg2.connect(dbname='postgres', user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{PG_DATABASE}'
        AND pid <> pg_backend_pid();
    """)
    cur.close()
    conn.close()
    print("✅ Existing connections terminated.")
except Exception as e:
    print(f"❌ Failed to terminate connections: {e}")
    sys.exit(1)

# === Drop and recreate the database ===
print("🧹 Dropping and recreating database...")

try:
    # Drop database
    subprocess.run(
        [PSQL_PATH, "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT, "-d", "postgres", "-c", f"DROP DATABASE IF EXISTS {PG_DATABASE};"],
        check=True
    )
    # Create database
    subprocess.run(
        [PSQL_PATH, "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT, "-d", "postgres", "-c", f"CREATE DATABASE {PG_DATABASE} WITH OWNER = {PG_USER} ENCODING = 'UTF8';"],
        check=True
    )
    print("✅ Database dropped and recreated.")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to drop/create database: {e}")
    sys.exit(1)

# === Restore the SQL file ===
print("📦 Restoring the SQL file...")

try:
    subprocess.run(
        [PSQL_PATH, "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT, "-d", PG_DATABASE, "-f", sql_file],
        check=True
    )
    print(f"✅ Restore completed for: {sql_file}")
except subprocess.CalledProcessError as e:
    print(f"❌ Restore failed: {e}")
    sys.exit(1)

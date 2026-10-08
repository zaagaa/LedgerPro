import os
import subprocess
import datetime
from pathlib import Path
import config
import sys

# === Add project path to sys.path ===
# backup.py is in BusinessApp/backup/, settings.py is in BusinessApp/BusinessApp/
BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up one level to BusinessApp/
sys.path.append(str(BASE_DIR))

# === Set Django settings module ===
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")  # Keep this as-is

# === Setup Django ===
import django
django.setup()

from django.conf import settings

# Get DB credentials from settings
db_settings = settings.DATABASES['default']
PG_USER = db_settings['USER']
PG_PASSWORD = db_settings['PASSWORD']
PG_DATABASE = db_settings['NAME']
PG_PORT = db_settings['PORT']
PG_HOST = db_settings['HOST']

#  The rest of your backup code continues here...
BACKUP_DIR = config.BACKUP_DIR

# === Network Backup Folder ===
# BACKUP_DIR = r"\\192.168.1.37\g\BACKUP_POST_SQL"
Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)

# === Generate backup filename ===
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"{PG_DATABASE}_backup_{timestamp}.sql"
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# === Full path to pg_dump ===
PG_DUMP_PATH = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"  #  Adjust if different version

# === Set PostgreSQL password env var ===
os.environ['PGPASSWORD'] = PG_PASSWORD

# === pg_dump command ===
cmd = [
    PG_DUMP_PATH,
    '-U', PG_USER,
    '-h', PG_HOST,
    '-p', PG_PORT,
    '-F', 'p',
    '-f', backup_path,
    PG_DATABASE
]

# === Run the backup ===
try:
    subprocess.run(cmd, check=True)
    print(f" Backup saved to: {backup_path}")
except subprocess.CalledProcessError as e:
    print(f"❌ Backup failed: {e}")
    exit()



# === Cleanup: Keep only latest 7 backups ===
MAX_BACKUPS = 24

# Get all backup files sorted by last modified time (oldest first)
backup_files = sorted(
    Path(BACKUP_DIR).glob(f"{PG_DATABASE}_backup_*.zip"),
    key=lambda f: f.stat().st_mtime
)

# Delete older backups
if len(backup_files) > MAX_BACKUPS:
    for old_file in backup_files[:-MAX_BACKUPS]:
        try:
            old_file.unlink()
            print(f"🗑️ Deleted old backup: {old_file}")
        except Exception as e:
            print(f"⚠️ Could not delete {old_file}: {e}")


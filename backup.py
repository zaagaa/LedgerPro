import os
import subprocess
import datetime
from pathlib import Path

# === PostgreSQL Config ===
PG_USER = 'postgres'
PG_PASSWORD = '123456'
PG_DATABASE = 'ledger_pro'
PG_PORT = '5462'
PG_HOST = 'localhost'

# === Network Backup Folder ===
BACKUP_DIR = r"\\192.168.1.37\g\BACKUP_POST_SQL"
Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)

# === Generate backup filename ===
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"{PG_DATABASE}_backup_{timestamp}.sql"
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# === Full path to pg_dump ===
PG_DUMP_PATH = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"  # ✅ Adjust if different version

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
    print(f"✅ Backup saved to: {backup_path}")
except subprocess.CalledProcessError as e:
    print(f"❌ Backup failed: {e}")
    exit()

# === Cleanup: Keep only latest 7 backups ===
MAX_BACKUPS = 7

# Get all backup files sorted by creation time (oldest first)
backup_files = sorted(
    Path(BACKUP_DIR).glob(f"{PG_DATABASE}_backup_*.sql"),
    key=os.path.getctime
)

# Delete older backups
if len(backup_files) > MAX_BACKUPS:
    for old_file in backup_files[:-MAX_BACKUPS]:
        try:
            os.remove(old_file)
            print(f"🗑️ Deleted old backup: {old_file}")
        except Exception as e:
            print(f"⚠️ Could not delete {old_file}: {e}")

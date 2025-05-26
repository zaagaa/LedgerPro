import os
import subprocess
import datetime
from pathlib import Path
import sys

# === Add project path to sys.path ===
BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up one level to BusinessApp/
sys.path.append(str(BASE_DIR))

# === Set Django settings module ===
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")

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

# === Define BACKUP_DIR above project ===
PROJECT_NAME = BASE_DIR.name
BACKUP_DIR = BASE_DIR / f"{PROJECT_NAME}_BACKUP"
print(BACKUP_DIR)
Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)


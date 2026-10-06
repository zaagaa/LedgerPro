import os
import django
import pytz
import datetime
from dotenv import load_dotenv
import dj_database_url

from collections import defaultdict
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS, models
from django.apps import apps
from django.utils.timezone import is_naive, make_aware

# === Setup Django ===
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

# === Constants ===
IST = pytz.timezone("Asia/Kolkata")
UTC = pytz.UTC
failed_records = defaultdict(list)

# === DB Setup ===
def get_online_db_url_from_setting():
    Setting = apps.get_model("setting", "Setting")
    try:
        setting_obj = Setting.objects.using(DEFAULT_DB_ALIAS).filter(setting="online_database_url").last()
        return setting_obj.value if setting_obj else None
    except Exception as e:
        print(f"❌ Failed to fetch 'online_database_url': {e}")
        return None

def configure_online_database():
    url = get_online_db_url_from_setting()
    if not url:
        print("❌ 'online_database_url' not found in Setting table.")
        return False
    try:
        db_config = dj_database_url.parse(url)
        db_config.setdefault('ATOMIC_REQUESTS', False)
        db_config.setdefault('AUTOCOMMIT', True)
        db_config.setdefault('CONN_MAX_AGE', 0)
        db_config.setdefault('OPTIONS', {})
        db_config.setdefault('TIME_ZONE', settings.TIME_ZONE)
        settings.DATABASES['online'] = db_config
        connections.databases['online'] = db_config
        return True
    except Exception as e:
        print(f"❌ Error configuring online DB: {e}")
        return False

def test_connection(alias):
    try:
        with connections[alias].cursor() as cursor:
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"✅ Connected to '{alias}' DB: {db_name}")
            return True
    except Exception as e:
        print(f"❌ Connection to '{alias}' failed: {e}")
        return False

def has_sync_fields(model_class):
    field_names = [f.name for f in model_class._meta.fields]
    return 'sync_offline' in field_names and 'sync_online' in field_names

def build_create_kwargs(obj):
    data = {}
    pk_field = obj._meta.pk.name
    for f in obj._meta.fields:
        if f.name == pk_field:
            continue
        val = getattr(obj, f.name)
        if isinstance(f, models.ForeignKey):
            data[f.name + "_id"] = val.pk if val else None
        elif isinstance(val, datetime.datetime):
            if is_naive(val):
                val = make_aware(val, IST)
            data[f.name] = val.astimezone(datetime.timezone.utc)
        else:
            data[f.name] = val
    data[pk_field] = getattr(obj, pk_field)
    return data

def sync_model(model_class):
    model_path = f"{model_class._meta.app_label}.{model_class.__name__}"
    pk_field = model_class._meta.pk.name

    print(f"\n🔄 Syncing: {model_path}")

    try:
        # Get latest timestamps
        offline_latest_sync_offline = model_class.objects.using('default').exclude(sync_offline__isnull=True).order_by('-sync_offline').values_list('sync_offline', flat=True).first() or 0
        online_latest_sync_offline = model_class.objects.using('online').exclude(sync_offline__isnull=True).order_by('-sync_offline').values_list('sync_offline', flat=True).first() or 0
        offline_latest_sync_online = model_class.objects.using('default').exclude(sync_online__isnull=True).order_by('-sync_online').values_list('sync_online', flat=True).first() or 0
        online_latest_sync_online = model_class.objects.using('online').exclude(sync_online__isnull=True).order_by('-sync_online').values_list('sync_online', flat=True).first() or 0

        print(f"🕒 offline.sync_offline = {offline_latest_sync_offline}")
        print(f"🕒 online.sync_offline  = {online_latest_sync_offline}")
        print(f"🕒 offline.sync_online = {offline_latest_sync_online}")
        print(f"🕒 online.sync_online  = {online_latest_sync_online}")
    except Exception as e:
        print(f"❌ Failed to get sync timestamps: {e}")
        return

    # === PASS 1: Upload offline ➝ online ===
    if offline_latest_sync_offline > online_latest_sync_offline:
        print(f"⬆️ Uploading: offline.sync_offline > online.sync_offline")
        offline_ids_to_upload = model_class.objects.using('default')\
            .filter(sync_offline__gt=online_latest_sync_offline)\
            .values_list(pk_field, flat=True)

        for obj_id in offline_ids_to_upload:
            try:
                local_obj = model_class.objects.using('default').get(**{pk_field: obj_id})
                online_exists = model_class.objects.using('online').filter(**{pk_field: obj_id}).exists()
                if not online_exists:
                    model_class.objects.using('online').create(**build_create_kwargs(local_obj))
                    print(f"⬆️ Created: {obj_id}")
                else:
                    model_class.objects.using('online').filter(**{pk_field: obj_id}).update(**build_create_kwargs(local_obj))
                    print(f"⬆️ Updated: {obj_id}")
            except Exception as e:
                print(f"❌ Upload error [{model_path} ID={obj_id}]: {e}")

    # === PASS 2: Download online ➝ offline ===
    if online_latest_sync_online > offline_latest_sync_online:
        print(f"⬇️ Downloading: online.sync_online > offline.sync_online")
        online_ids_to_download = model_class.objects.using('online')\
            .filter(sync_online__gt=offline_latest_sync_online)\
            .values_list(pk_field, flat=True)

        for obj_id in online_ids_to_download:
            try:
                online_obj = model_class.objects.using('online').get(**{pk_field: obj_id})
                offline_exists = model_class.objects.using('default').filter(**{pk_field: obj_id}).exists()
                if not offline_exists:
                    model_class.objects.using('default').create(**build_create_kwargs(online_obj))
                    print(f"⬇️ Created: {obj_id}")
                else:
                    model_class.objects.using('default').filter(**{pk_field: obj_id}).update(**build_create_kwargs(online_obj))
                    print(f"⬇️ Updated: {obj_id}")
            except Exception as e:
                print(f"❌ Download error [{model_path} ID={obj_id}]: {e}")

def main():
    print("📡 Starting TWO-WAY SYNC (offline ➝ online ➝ offline)...\n")

    if not test_connection('default'):
        print("⛔ Local DB connection failed.")
        return

    if not configure_online_database() or not test_connection('online'):
        print("⛔ Online DB setup or connection failed.")
        return

    eligible_models = [
        m for m in apps.get_models()
        if has_sync_fields(m)
    ]

    print(f"\n📋 {len(eligible_models)} models eligible for sync\n")

    for model_class in eligible_models:
        sync_model(model_class)

    print("\n✅ Full TWO-WAY Sync Complete.")

if __name__ == "__main__":
    main()

import os
import django
import pytz
import time
import datetime  # ✅ Fix: import added
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
failed_records = defaultdict(list)  # model_label → (obj, source)

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

# === Column Checks ===
def has_db_column(model_class, db_alias, column_name):
    table = model_class._meta.db_table
    with connections[db_alias].cursor() as cursor:
        try:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", [table])
            columns = [row[0] for row in cursor.fetchall()]
            return column_name in columns
        except Exception as e:
            print(f"⚠️ Failed to check columns for {table} on {db_alias}: {e}")
            return False

def is_sync_eligible(model_class):
    if 'sync_unix' not in [f.name for f in model_class._meta.fields]:
        return False
    return has_db_column(model_class, 'default', 'sync_unix') and has_db_column(model_class, 'online', 'sync_unix')

# === Utility ===
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
    if hasattr(obj, 'sync_unix'):
        data['sync_unix'] = getattr(obj, 'sync_unix')
    return data

def get_max_sync_unix(model_class, db_alias):
    try:
        return model_class.objects.using(db_alias).order_by('-sync_unix').values_list('sync_unix', flat=True).first() or 0
    except:
        return 0

# === Core Sync Logic ===
def sync_model(model_class):
    model_path = f"{model_class._meta.app_label}.{model_class.__name__}"
    print(f"\n🔄 Syncing: {model_path}")
    pk_field = model_class._meta.pk.name

    latest_local = get_max_sync_unix(model_class, 'default')
    latest_online = get_max_sync_unix(model_class, 'online')

    if latest_local == latest_online:
        print(f"✅ Skipped (nothing changed): {model_path}")
        return

    sync_threshold = min(latest_local, latest_online)

    try:
        local_ids = list(
            model_class.objects.using('default')
            .filter(sync_unix__gt=sync_threshold)
            .values_list(pk_field, flat=True)
        )

        online_ids = list(
            model_class.objects.using('online')
            .filter(sync_unix__gt=sync_threshold)
            .values_list(pk_field, flat=True)
        )

        all_ids = set(str(i) for i in local_ids) | set(str(i) for i in online_ids)
    except Exception as e:
        print(f"❌ Failed to fetch IDs for {model_path}: {e}")
        return

    for obj_id in all_ids:
        try:
            local_obj = model_class.objects.using('default').filter(**{pk_field: obj_id}).first()
            online_obj = model_class.objects.using('online').filter(**{pk_field: obj_id}).first()

            if local_obj and not online_obj:
                try:
                    model_class.objects.using('online').create(**build_create_kwargs(local_obj))
                    print(f"⬆️ Uploaded new: {obj_id}")
                except Exception as e:
                    print(f"❌ Upload failed: {obj_id} → {e}")
                    failed_records[model_path].append((local_obj, 'local'))

            elif online_obj and not local_obj:
                try:
                    model_class.objects.using('default').create(**build_create_kwargs(online_obj))
                    print(f"⬇️ Downloaded new: {obj_id}")
                except Exception as e:
                    print(f"❌ Download failed: {obj_id} → {e}")
                    failed_records[model_path].append((online_obj, 'online'))

            elif local_obj and online_obj:
                local_time = local_obj.sync_unix or 0
                online_time = online_obj.sync_unix or 0

                print(f"⏱ Comparing sync_unix:\n  Local : {local_time}\n  Online: {online_time}")

                if local_time == online_time:
                    print(f"✅ Skipped (same): {obj_id}")
                    continue

                source = 'local' if local_time > online_time else 'online'
                source_obj = local_obj if source == 'local' else online_obj
                target_db = 'online' if source == 'local' else 'default'
                values = {}
                for f in source_obj._meta.fields:
                    if f.name == pk_field:
                        continue
                    val = getattr(source_obj, f.name)
                    if isinstance(val, models.Model):
                        val = val.pk
                    elif isinstance(val, datetime.datetime):
                        if is_naive(val):
                            val = make_aware(val, IST)
                        val = val.astimezone(datetime.timezone.utc)
                    values[f.name] = val
                values['sync_unix'] = getattr(source_obj, 'sync_unix')

                try:
                    model_class.objects.using(target_db).filter(**{pk_field: obj_id}).update(**values)
                    print(f"⚡ {source} newer → Updated {target_db}: {obj_id}")
                except Exception as e:
                    print(f"❌ Update failed: {obj_id} → {e}")
                    failed_records[model_path].append((source_obj, source))

        except Exception as e:
            print(f"❌ Error during sync of {model_path} ID {obj_id}: {e}")

# === Retry Failed Records ===
def retry_failed_creations():
    if not failed_records:
        return
    print("\n🔁 Retrying failed records...\n")

    for model_path, record_list in failed_records.items():
        app_label, model_name = model_path.split(".")
        model_class = apps.get_model(app_label, model_name)
        pk_field = model_class._meta.pk.name

        for obj, source in record_list:
            try:
                target_db = 'online' if source == 'local' else 'default'
                model_class.objects.using(target_db).create(**build_create_kwargs(obj))
                print(f"✅ Retry success: {model_path} {getattr(obj, pk_field)}")
            except Exception as e:
                print(f"❌ Retry failed: {model_path} {getattr(obj, pk_field)} → {e}")

# === Entry Point ===
def main():
    print("📱 Starting DB sync between offline (default) and online databases...\n")

    if not test_connection('default'):
        print("⛔ Local DB connection failed.")
        return

    if not configure_online_database() or not test_connection('online'):
        print("⛔ Online DB setup or connection failed.")
        return

    all_models = apps.get_models()
    eligible_models = []
    for model in all_models:
        try:
            if is_sync_eligible(model):
                eligible_models.append(model)
            else:
                print(f"⚠️ Skipped: {model._meta.label} (missing sync_unix in DB)")
        except Exception as e:
            print(f"⚠️ Error checking {model._meta.label}: {e}")

    print(f"\n📋 {len(eligible_models)} model(s) eligible for sync\n")

    for model_class in eligible_models:
        sync_model(model_class)

    retry_failed_creations()
    print("\n✅ Sync complete.")

if __name__ == "__main__":
    main()

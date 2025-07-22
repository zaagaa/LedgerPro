from django.db import models
import os
import django
import pytz
from dotenv import load_dotenv
import dj_database_url
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None



from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS, models
from django.apps import apps
from django.db.models import DateTimeField, Q
from django.utils.timezone import is_naive, now
from datetime import datetime, timedelta

# === Setup Django environment ===
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

# === Constants ===
IST = pytz.timezone("Asia/Kolkata")
UTC = pytz.UTC
SYNC_LIMIT_DAYS = 10  # 0 = full sync, N = last N days

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

def is_sync_eligible(model_class):
    return any(field.name == 'sync' and isinstance(field, DateTimeField) for field in model_class._meta.fields)

def test_connection(alias):
    try:
        with connections[alias].cursor() as cursor:
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f" Connected to '{alias}' DB: {db_name}")
            return True
    except Exception as e:
        print(f"❌ Connection to '{alias}' failed: {e}")
        return False

def get_utc_time(val, assume_timezone):
    if not val:
        return datetime.min.replace(tzinfo=UTC)
    if is_naive(val):
        val = assume_timezone.localize(val)
    return val.astimezone(UTC)

def build_create_kwargs(obj):
    data = {}
    for f in obj._meta.fields:
        if f.name == 'id':
            continue
        val = getattr(obj, f.name)
        if isinstance(f, models.ForeignKey):
            data[f.name + "_id"] = val.pk if val else None
        else:
            data[f.name] = val
    data['id'] = obj.id
    return data

def sync_model(model_class):
    model_path = f"{model_class._meta.app_label}.{model_class.__name__}"
    print(f"\n🔄 Syncing: {model_path}")

    try:
        offline_filter = Q()
        online_filter = Q()
        if SYNC_LIMIT_DAYS > 0:
            cutoff = now() - timedelta(days=SYNC_LIMIT_DAYS)
            offline_filter = Q(updated_at__gte=cutoff.astimezone(IST))
            online_filter = Q(updated_at__gte=cutoff.astimezone(UTC))

        local_qs = model_class.objects.using('default').filter(offline_filter).order_by('-updated_at')
        online_qs = model_class.objects.using('online').filter(online_filter).order_by('-updated_at')
    except Exception as e:
        print(f"❌ Failed to load data for {model_path}: {e}")
        return

    local_data = {str(obj.id): obj for obj in local_qs}
    online_data = {str(obj.id): obj for obj in online_qs}
    all_ids = set(local_data.keys()) | set(online_data.keys())

    for obj_id in all_ids:
        local_obj = local_data.get(obj_id)
        online_obj = online_data.get(obj_id)

        try:
            if local_obj and not online_obj:
                if not model_class.objects.using('online').filter(id=obj_id).exists():
                    model_class.objects.using('online').create(**build_create_kwargs(local_obj))
                    print(f"⬆️ Uploaded new: {obj_id}")
                else:
                    print(f"⚠️ Skipped (already exists in online): {obj_id}")

            elif online_obj and not local_obj:
                if not model_class.objects.using('default').filter(id=obj_id).exists():
                    model_class.objects.using('default').create(**build_create_kwargs(online_obj))
                    print(f"⬇️ Downloaded new: {obj_id}")
                else:
                    print(f"⚠️ Skipped (already exists in offline): {obj_id}")

            elif local_obj and online_obj:
                local_time = get_utc_time(local_obj.updated_at, IST)
                online_time = get_utc_time(online_obj.updated_at, UTC)

                print(f"⏱ Comparing updated_at:\n  Local : {local_time} ({local_time.microsecond})\n  Online: {online_time} ({online_time.microsecond})")

                if local_time == online_time:
                    print(f" Skipped (already same): {obj_id}")
                    continue

                if local_time > online_time:
                    values = {}
                    has_diff = False
                    for f in local_obj._meta.fields:
                        if f.name == 'id':
                            continue
                        local_val = getattr(local_obj, f.name)
                        online_val = getattr(online_obj, f.name)
                        if isinstance(local_val, models.Model):
                            local_val = local_val.pk
                        if isinstance(online_val, models.Model):
                            online_val = online_val.pk
                        values[f.name] = local_val
                        if local_val != online_val and f.name != "updated_at":
                            has_diff = True
                    values['updated_at'] = local_obj.updated_at
                    if has_diff:
                        model_class.objects.using('online').filter(id=obj_id).update(**values)



                        print(f"⚡ Local newer → Updated Online: {obj_id}")
                    else:
                        model_class.objects.using('online').filter(id=obj_id).update(updated_at=local_obj.updated_at)



                        print(f"🛠 Synced updated_at only for: {obj_id}")

                elif online_time > local_time:
                    values = {}
                    has_diff = False
                    for f in online_obj._meta.fields:
                        if f.name == 'id':
                            continue
                        online_val = getattr(online_obj, f.name)
                        local_val = getattr(local_obj, f.name)
                        if isinstance(online_val, models.Model):
                            online_val = online_val.pk
                        if isinstance(local_val, models.Model):
                            local_val = local_val.pk
                        values[f.name] = online_val
                        if online_val != local_val and f.name != "updated_at":
                            has_diff = True
                    values['updated_at'] = online_obj.updated_at
                    if has_diff:
                        model_class.objects.using('default').filter(id=obj_id).update(**values)



                        print(f"⚡ Online newer → Updated Local: {obj_id}")
                    else:
                        model_class.objects.using('default').filter(id=obj_id).update(updated_at=online_obj.updated_at)



                        print(f"🛠 Synced updated_at only for: {obj_id}")

        except Exception as e:
            print(f"❌ Sync error in {model_path} for ID {obj_id}: {e}")

def main():
    print("📱 Starting DB sync between offline (default) and online databases...\n")

    if not test_connection('default'):
        print("⛔ Local DB connection failed.")
        return

    if not configure_online_database() or not test_connection('online'):
        print("⛔ Online DB setup or connection failed.")
        return

    all_models = apps.get_models()
    eligible_models = [m for m in all_models if is_sync_eligible(m)]

    print(f"\n📋 {len(eligible_models)} model(s) eligible for sync (limit={SYNC_LIMIT_DAYS} day(s), latest first).\n")

    for model_class in eligible_models:
        sync_model(model_class)

    print("\n Sync complete.")

if __name__ == "__main__":
    main()


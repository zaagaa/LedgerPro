import os
import django
import pytz
from dotenv import load_dotenv
import dj_database_url

from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from django.apps import apps
from django.db.models import DateTimeField, ForeignKey
from django.utils.timezone import make_aware, now
from datetime import timedelta

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

IST = pytz.timezone('Asia/Kolkata')
UTC = pytz.UTC


def get_online_db_url_from_setting():
    Setting = apps.get_model("setting", "Setting")
    try:
        setting_obj = Setting.objects.using(DEFAULT_DB_ALIAS).filter(setting="online_database_url").last()
        return setting_obj.value if setting_obj else None
    except Exception as e:
        print(f"❌ Failed to fetch 'online_database_url' from Setting model: {e}")
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
            print(f" Connected to '{alias}' DB: {db_name}")
            return True
    except Exception as e:
        print(f"❌ Connection to '{alias}' failed: {e}")
        return False


def is_sync_eligible(model_class):
    return any(field.name == 'sync' and isinstance(field, DateTimeField) for field in model_class._meta.fields)


def convert_to_utc(dt, source_tz):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = make_aware(dt, source_tz)
    return dt.astimezone(UTC)


def extract_field_values(obj, model_class, target_db):
    fields = {}
    for field in model_class._meta.fields:
        if field.name == 'id':
            continue
        try:
            value = getattr(obj, field.name)
            if field.is_relation and isinstance(field, ForeignKey) and value is not None:
                if isinstance(value, field.related_model) and value._state.db != target_db:
                    value = field.related_model.objects.using(target_db).get(pk=value.pk)
                elif not isinstance(value, field.related_model):
                    value = field.related_model.objects.using(target_db).get(pk=value)
            fields[field.name] = value
        except Exception as e:
            print(f"⚠️ Skipped field {field.name} due to error: {e}")
    return fields


def save_preserving_updated_at(model_class, pk, fields, db_alias):
    try:
        if model_class.objects.using(db_alias).filter(pk=pk).exists():
            model_class.objects.using(db_alias).filter(pk=pk).update(**fields)



        else:
            model_class.objects.using(db_alias).create(pk=pk, **fields)
    except Exception as e:
        print(f"❌ DB write error for {model_class.__name__} [{pk}] on {db_alias}: {e}")


def sync_model(model_class):
    model_path = f"{model_class._meta.app_label}.{model_class.__name__}"
    print(f"\n🔄 Syncing: {model_path}")

    if not hasattr(model_class, 'updated_at'):
        print(f"⏭️ Skipping {model_path} (no 'updated_at' field)")
        return

    try:
        threshold = now() - timedelta(hours=24)

        # IDs of recently updated records
        local_recent_ids = set(
            model_class.objects.using('default')
            .filter(updated_at__gte=threshold)
            .values_list('id', flat=True)
        )
        online_recent_ids = set(
            model_class.objects.using('online')
            .filter(updated_at__gte=threshold)
            .values_list('id', flat=True)
        )

        # All IDs from both DBs
        all_offline_ids = set(
            model_class.objects.using('default').values_list('id', flat=True)
        )
        all_online_ids = set(
            model_class.objects.using('online').values_list('id', flat=True)
        )

        # Merge all relevant IDs
        all_ids = local_recent_ids | online_recent_ids | (all_offline_ids - all_online_ids) | (all_online_ids - all_offline_ids)

        # Fetch records for those IDs
        local_data = {
            str(obj.id): obj
            for obj in model_class.objects.using('default').filter(id__in=all_ids)
        }
        online_data = {
            str(obj.id): obj
            for obj in model_class.objects.using('online').filter(id__in=all_ids)
        }

    except Exception as e:
        print(f"❌ Failed to load data for {model_path}: {e}")
        return

    for obj_id in all_ids:
        local_obj = local_data.get(str(obj_id))
        online_obj = online_data.get(str(obj_id))

        try:
            if local_obj and not online_obj:
                fields = extract_field_values(local_obj, model_class, 'online')
                save_preserving_updated_at(model_class, obj_id, fields, 'online')
                print(f"⬆️ Uploaded: {obj_id}")

            elif online_obj and not local_obj:
                fields = extract_field_values(online_obj, model_class, 'default')
                save_preserving_updated_at(model_class, obj_id, fields, 'default')
                print(f"⬇️ Downloaded: {obj_id}")

            elif local_obj and online_obj:
                local_time = convert_to_utc(getattr(local_obj, 'updated_at', None), IST)
                online_time = convert_to_utc(getattr(online_obj, 'updated_at', None), UTC)

                if local_time and online_time and abs((local_time - online_time).total_seconds()) > 1:
                    if local_time > online_time:
                        fields = extract_field_values(local_obj, model_class, 'online')
                        save_preserving_updated_at(model_class, obj_id, fields, 'online')
                        print(f"⚡ Local newer → Updated Online: {obj_id}")
                    else:
                        fields = extract_field_values(online_obj, model_class, 'default')
                        save_preserving_updated_at(model_class, obj_id, fields, 'default')
                        print(f"⚡ Online newer → Updated Local: {obj_id}")

        except Exception as e:
            print(f"❌ Sync error in {model_path} for ID {obj_id}: {e}")


def main():
    print("📡 Starting DB sync between offline (default) and online databases...\n")

    if not test_connection('default'):
        print("⛔ Local DB connection failed.")
        return

    if not configure_online_database() or not test_connection('online'):
        print("⛔ Online DB setup or connection failed.")
        return

    #  Models to be skipped from sync
    EXCLUDED_MODELS = {
        "pos.UnprintedSaleLog",
        "pos.FieldChangeLog"
        # Add more here
    }

    all_models = apps.get_models()
    eligible_models = [
        m for m in all_models
        if is_sync_eligible(m) and f"{m._meta.app_label}.{m.__name__}" not in EXCLUDED_MODELS
    ]

    print(f"\n📋 {len(eligible_models)} model(s) eligible for sync.\n")

    for model_class in eligible_models:
        sync_model(model_class)

    print("\n Sync complete.")


if __name__ == "__main__":
    main()

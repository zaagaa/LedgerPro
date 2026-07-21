from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import os
from threading import Lock
from setting.views import get_setting


from setting.upload_into_s3 import retry_failed_s3_uploads, cleanup_deleted_images_from_s3

# Optional: lock for external visibility
sync_lock = Lock()

# Import from views.py
from scheduler.views import run_sync_script, deactivate_inactive_customers, send_sms_alert, biometric_device

_scheduler_started = False

def start():
    global _scheduler_started
    if _scheduler_started:
        return
    _scheduler_started = True

    scheduler = BackgroundScheduler()

    # Run sync_db.py every 2 minutes (offline only)
    scheduler.add_job(
        run_sync_script,
        trigger=IntervalTrigger(minutes=10),
        id='sync_job',
        max_instances=1,
        coalesce=True
    )

    # Deactivate inactive customers every 3 hours
    scheduler.add_job(
        deactivate_inactive_customers,
        trigger=CronTrigger(hour='*/3', minute=0),
        id='deactivate_customers',
        replace_existing=True
    )

    # Upload into S3, If Any Failed Image Found
    scheduler.add_job(
        retry_failed_s3_uploads,
        trigger=IntervalTrigger(minutes=30),
        max_instances=1,
        coalesce=True
    )

    # Delete S3 Image, If image deleted in offline, every 6 hours
    scheduler.add_job(
        cleanup_deleted_images_from_s3,
        trigger=CronTrigger(hour='*/6', minute=0),
        max_instances=1,
        coalesce=True
    )

    # SMS ALERT to customer every 2 hours
    scheduler.add_job(
        send_sms_alert,
        trigger=CronTrigger(hour='*/2', minute=0),
        max_instances=1,
        coalesce=True
    )

    # Run sync_db.py every 2 minutes (offline only)
    scheduler.add_job(
        biometric_device,
        trigger=IntervalTrigger(minutes=int(get_setting("biometric_import_duration")) or 2),
        max_instances=1,
        coalesce=True
    )

    scheduler.start()
    print("APScheduler started:")
    print("sync_db.py every 2 mins (offline only)")
    print("deactivate_inactive_customers every 3 hours")

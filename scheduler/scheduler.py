from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import os
from threading import Lock

# Optional: lock for external visibility
sync_lock = Lock()

# Import from views.py
from scheduler.views import run_sync_script, deactivate_inactive_customers

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
        trigger=IntervalTrigger(minutes=2),
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

    scheduler.start()
    print("APScheduler started:")
    print("sync_db.py every 2 mins (offline only)")
    print("deactivate_inactive_customers every 3 hours")

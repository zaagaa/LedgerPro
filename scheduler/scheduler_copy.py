from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import subprocess
import time
import os
import sys

def run_sync_script():
    if os.getenv("DATABASE_URL"):
        print(f"⏩ Skipped sync_db.py at {time.ctime()} (online mode detected)")
        return

    print(f"🔁 Running sync_db.py at {time.ctime()} (offline mode detected)")

    python_path = sys.executable
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sync_db.py")
    script_path = os.path.abspath(script_path)

    try:
        subprocess.run([python_path, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ sync_db.py failed: {e}")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_sync_script, IntervalTrigger(minutes=1))
    scheduler.start()
    print("✅ APScheduler started to run sync_db.py every 1 minute (only if offline)")

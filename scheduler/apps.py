from django.apps import AppConfig
import threading
import os

class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":  # ✅ Avoid duplicate scheduler
            from .scheduler import start
            threading.Thread(target=start, daemon=True).start()

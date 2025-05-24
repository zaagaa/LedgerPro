import datetime
from pos.models import UnprintedSaleLog
from django.utils.timezone import now

class AutoDeleteUnprintedLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_cleanup = None

    def __call__(self, request):
        # Run once per day per server run
        today = now().date()
        if self.last_cleanup != today:
            self.last_cleanup = today
            try:
                days = int(request.setting_value("unprinted_log_delete") or 30)
                cutoff = now() - datetime.timedelta(days=days)
                deleted_count, _ = UnprintedSaleLog.objects.filter(created_at__lt=cutoff).delete()
                print(f"[AUTO DELETE] 🧹 Removed {deleted_count} old unprinted logs older than {days} days.")
            except Exception as e:
                print(f"[AUTO DELETE] ❌ Failed: {e}")

        return self.get_response(request)

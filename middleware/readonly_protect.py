import threading
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, "request", None)

class ReadOnlyProtectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.request = request

        # ✅ Only enforce read-only in online environment
        if getattr(settings, "INSTANCE_TYPE", "") != "online":
            return

        if not request.user.is_authenticated:
            return

        if request.user.is_superuser:
            return

        if request.method == "GET":
            return

        if request.path.startswith("/authenticate"):
            return

        if request.session.get("_readonly", False):
            messages.warning(request, "❌ You are in read-only mode. Write access is blocked.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

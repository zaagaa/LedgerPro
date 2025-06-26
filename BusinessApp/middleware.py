import time


from django.http import HttpResponse

from authentication.models import User
from company.models import Company

import socket

import time
from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, get_user_model


class PageLoadTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._start_time = time.time()
        response = self.get_response(request)

        content_type = response.get('Content-Type', '')
        if 'text/html' in content_type and hasattr(response, 'content'):
            duration = round(time.time() - request._start_time, 3)
            try:
                content = response.content.decode('utf-8')
                if '</body>' in content:
                    # Inject hidden server time for JS to pick up
                    injected_html = (
                        f'<div class="load-time-server d-none" data-time="{duration}"></div></body>'
                    )
                    content = content.replace('</body>', injected_html)
                    response.content = content.encode('utf-8')
            except Exception as e:
                print("[PageLoadTimeMiddleware error]", e)

        return response


class AutoLockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        now = time.time()
        last_verified = request.session.get("last_verified_time")
        verified = request.session.get("verified", False)

        if verified and last_verified and now - last_verified > 60:  # 1 minute
            request.session["verified"] = False  # auto-lock
        if verified:
            request.session["last_verified_time"] = now


# class UserActivityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def get_local_ip(self):
#         try:
#             s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             s.connect(("8.8.8.8", 80))
#             local_ip = s.getsockname()[0]
#             s.close()
#         except Exception:
#             local_ip = '127.0.0.1'
#         return local_ip
#
#     def __call__(self, request):
#         response = self.get_response(request)
#
#         if request.user.is_authenticated:
#             ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
#             local_ip = self.get_local_ip()
#             pc_name = socket.gethostname()
#
#             # UserActivity.objects.create(
#             #     user=request.user,
#             #     path=request.path,
#             #     method=request.method,
#             #     ip_address=ip_address,
#             #     local_ip_address=local_ip,
#             #     pc_name=pc_name
#             # )
#
#         return response

User = get_user_model()

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        User = get_user_model()



        # ✅ Restore Logic
        if request.path.startswith("/setting/backup/restore/"):
            response = self.get_response(request)
            return response

        # # ✅ Static Logic
        # if request.path.startswith("/static/"):
        #     response = self.get_response(request)
        #     return response


        # ✅ Unauthenticated user logic
        if not request.user.is_authenticated and not request.path.startswith("/authenticate/"):
            user_count = User.objects.filter(is_superuser=True).count()
            if user_count > 0:
                return redirect("login")
            else:
                return redirect("signup")



        # ✅ Logout logic
        if request.path.endswith("/logout/"):

            logout(request)
            response = HttpResponseRedirect("/login/")
            response.delete_cookie("company_id")
            return response

        # ✅ Bypass redirect if impersonating
        is_impersonating = request.session.get("impersonator_id") is not None

        # ✅ POS user redirect
        if request.user.is_authenticated and request.user.position == 2:
            if not is_impersonating and not request.path.startswith("/pos/") and not request.path.startswith("/qrcode/"):
                return redirect("pos")

        # ✅ Point user redirect
        if request.user.is_authenticated and request.user.position == 3:
            if not is_impersonating and not request.path.startswith("/customer/points/"):
                return redirect("customer_point")

        # ✅ Proceed to view
        response = self.get_response(request)

        # ✅ Force company creation only for non-impersonating users
        if request.user.is_authenticated and not is_impersonating:
            company_count = Company.objects.count()
            if company_count == 0 and not request.path.startswith("/company/"):
                return redirect("company_index")

        # ✅ Set default company_id cookie if not present
        if request.user.is_authenticated and not is_impersonating:
            if request.COOKIES.get("company_id") is None:
                if request.user.is_superuser:
                    company = Company.objects.order_by("id").first()
                else:
                    company = request.user.company

                if company:
                    response.set_cookie("company_id", str(company.id))

        return response




from django.http import HttpResponseForbidden
from django.utils.html import format_html

class ElectronOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        # print(request.headers.get('X-Electron-App'), "request.headers.get('X-Electron-App')")
        # print(user.is_authenticated,"user.is_authenticated")
        # print(user.position,"user.position")
        if user.is_authenticated and not user.is_superuser:
            print(request.headers.get('X-Electron-App'),"request.headers.get('X-Electron-App')")
            if request.headers.get('X-Electron-App') != 'yes':
                logout_url = '/logout/'  # Change this if your logout URL is different
                message = format_html(
                    "Access denied. Use the official desktop app. <a href='{}'>Logout</a>", logout_url
                )
                return HttpResponseForbidden(message)

        return self.get_response(request)


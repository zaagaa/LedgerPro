from .models import Setting  # adjust this import to your actual path

from django.conf import settings

class SettingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add dynamic sync_field to request
        request.sync_field = "sync_offline" if settings.INSTANCE_TYPE == "offline" else "sync_online"

        # Existing setting methods
        request.setting_value = self._setting_value(request)
        request.setting_update = self._setting_update(request)

        return self.get_response(request)

    def _setting_value(self, request):
        def inner(setting_key):
            company_id = request.COOKIES.get('company_id')
            setting_obj = Setting.objects.filter(company_id=company_id, setting=setting_key).last()
            if not setting_obj:
                setting_obj = Setting.objects.filter(company_id=None, setting=setting_key).last()
            return getattr(setting_obj, 'value', None)
        return inner


    def _setting_update(self, request):
        def inner(setting_key, value):
            company_id = request.COOKIES.get('company_id')

            # Check for company-specific setting
            setting_obj = Setting.objects.filter(company_id=company_id, setting=setting_key).last()
            if not setting_obj:
                # Fallback to global setting
                setting_obj = Setting.objects.filter(company_id=None, setting=setting_key).last()

            if setting_obj:
                # Skip if value is already same
                if setting_obj.value == value:
                    return value
                # Update value and trigger pre_save (to update sync field)
                setting_obj.value = value
                setting_obj.save()
            else:
                # Create new if no existing setting
                Setting.objects.create(company_id=company_id, setting=setting_key, value=value)

            return value

        return inner


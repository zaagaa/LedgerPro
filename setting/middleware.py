from .models import Setting  # adjust this import to your actual path

class SettingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Attach methods to request
        request.setting_value = self.setting_value.__get__(request)
        request.setting_update = self.setting_update.__get__(request)
        return self.get_response(request)

    # def setting_value(self, setting_key):
    #     company_id = self.COOKIES.get('company_id')
    #     try:
    #         return Setting.objects.filter(company_id=company_id, setting=setting_key).last().value
    #     except:
    #         return Setting.objects.filter(company_id=None, setting=setting_key).last().value

    def setting_value(self, setting_key):
        company_id = self.COOKIES.get('company_id')
        setting_obj = Setting.objects.filter(company_id=company_id, setting=setting_key).last()
        if not setting_obj:
            setting_obj = Setting.objects.filter(company_id=None, setting=setting_key).last()
        return getattr(setting_obj, 'value', None)

    # def setting_update(self, setting_key, value):
    #     company_id = self.COOKIES.get('company_id')
    #     updated = Setting.objects.filter(company_id=company_id, setting=setting_key).update(value=value)
    #     if updated == 0:
    #         Setting.objects.filter(company_id=None, setting=setting_key).update(value=value)
    #     return value

    def setting_update(self, setting_key, value):
        company_id = self.COOKIES.get('company_id')
        updated = Setting.objects.filter(company_id=company_id, setting=setting_key).update(value=value)

        if updated == 0:
            updated = Setting.objects.filter(company_id=None, setting=setting_key).update(value=value)

        if updated == 0:
            Setting.objects.create(company_id=company_id, setting=setting_key, value=value)

        return value

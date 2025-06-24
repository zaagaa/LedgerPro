from setting.models import Setting, Master_Setting
from sync.models import Deleted_Record
from django.db import connection

def invoice_type():
    db_settings = connection.settings_dict
    db_name = db_settings.get('NAME', '')
    db_host = db_settings.get('HOST', '')

    # Check if Railway (online)
    if 'railway' in db_name or 'railway' in db_host or 'proxy.rlwy.net' in db_host:
        return 2  # online
    return 1  # offline

#DEFAULT SETTING INSTALL FUNCTION

# def default_setting_install(company_id):
#     install_setting(company_id, "barcode_method", "{YEAR}A{ID}")
#     install_setting(company_id, "pos_round_off", "60")
#     install_setting(company_id, "pos_footer", '<div align="center">THANK YOU! VISIT AGAIN!</div>')
#     install_setting(company_id, "currency_denomination", '2000;500;200;100;50;20;10;5;2;1')
#     install_setting(company_id, "bundle_transport", 'BLUEDART;DHL;AKR;RATHIMEENA;METTUR;')
#     install_setting(company_id, "currency_symbol", '₹')
#     install_setting(company_id, "currency_decimal", '2')
#
#
# def install_setting(company_id,setting,value):
#     if not Setting.objects.filter(setting=setting, company=company_id).exists():
#         Setting(setting=setting, value=value, company_id=company_id).save()
#         return value
#     else:
#         return Setting.objects.get(setting=setting, company=company_id).value

#END DEFAULT SETTING INSTALL FUNCTION


#
# #DEFAULT *MASTER* SETTING INSTALL FUNCTION
#
# def default_master_setting_install():
#     install_master_setting("software_type", "master")
#
#
#
# def install_master_setting(setting,value):
#     if not Master_Setting.objects.filter(setting=setting).exists():
#         Master_Setting(setting=setting, value=value).save()
#         return value
#     else:
#         return Master_Setting.objects.get(setting=setting).value
#
# #END DEFAULT *MASTER* SETTING INSTALL FUNCTION

# def deleted_record(model, delete_query):
#     """
#     Records deleted model entries for sync purposes.
#
#     :param model: Django model class
#     :param delete_query: QuerySet of objects to be deleted
#     """
#     app_label = model._meta.app_label
#     model_name = model._meta.object_name
#     deleted_ids = []
#
#     for obj in delete_query:
#         deleted_ids.append(obj.id)
#         # Track deletion
#         Deleted_Record.objects.create(
#             app_name=app_label,
#             model_name=model_name,
#             model_id=str(obj.id)  # convert UUID to string if needed
#         )
#         # Delete the object
#         obj.delete()
#
#     print(f"🗑️ Deleted from {app_label}.{model_name}: {deleted_ids}")



# def deleted_record(model,delete_query):
#     print(model._meta.app_label)
#     deleted = []
#     for item in delete_query:
#         deleted.append(item.id)
#         Deleted_Record(app_name=model._meta.app_label, model_name=model._meta.object_name, model_id=item.id).save()
#         item.delete()
#     print(deleted)

def decimal_value(number):
    return float('%.2f' % (number))


def int_value(value):
    value=float(value)
    if value==int(value):
        return int(value)
    else:
        return decimal_value(value)

# def setting_value(request,setting):
#     try:
#         setting=Setting.objects.filter(company_id=request.COOKIES.get('company_id'), setting=setting).last().value
#         return setting
#     except:
#         setting=Setting.objects.filter(company_id=None, setting=setting).last().value
#         return setting
#
#
# def setting_update(request, setting_key, value):
#     company_id = request.COOKIES.get('company_id')
#
#     updated = Setting.objects.filter(company_id=company_id, setting=setting_key).update(value=value)
#     if updated == 0:
#         # fallback to global setting
#         Setting.objects.filter(company_id=None, setting=setting_key).update(value=value)
#
#     return value
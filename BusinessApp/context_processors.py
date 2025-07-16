from authentication.models import User
from company.models import Company
from setting.models import Setting, Master_Setting
import datetime


from django.conf import settings
from django.utils import timezone

from django.urls import resolve

def url_name_to_title(request):
    try:
        url_name = resolve(request.path_info).url_name
        if url_name:
            title = url_name.replace('_', ' ').title()
        else:
            title = 'Untitled Page'
    except Exception:
        title = 'Page'

    return {'page_title': title}



def version_context(request):
    return {
        "VERSION": settings.VERSION
    }


def context_processor(request):



    if request.user.is_authenticated:

        context = {

        }



        try:
            if request.COOKIES.get('company_id') is None:
                CURRENT_COMPANY = Company.objects.get(id=request.user.company.id)
            else:
                CURRENT_COMPANY = Company.objects.get(id=request.COOKIES.get('company_id'))
                print(request.COOKIES.get('company_id'), "COOKIE")
        except:
            CURRENT_COMPANY = Company.objects.order_by('id').first()




        try:
            COMPANY_LIST=Company.objects.all()
        except:
            COMPANY_LIST=''

        try:
            COMPANY=CURRENT_COMPANY

            if COMPANY.tax_type == 'Gst':
                request.session["TAX_CODE_NAME"] = "Hsn"
            elif COMPANY.tax_type == 'Vat':
                request.session["TAX_CODE_NAME"] = "Commodity"
            else:
                request.session["TAX_CODE_NAME"] = "***"

        except:
            COMPANY=''



        try:
            setting_data={}
            setting_list=Setting.objects.filter(company_id=CURRENT_COMPANY.id)
            for data in setting_list:
                setting_data[data.setting]=data.value

            setting_list=Setting.objects.filter(company_id=None)
            for data in setting_list:
                setting_data[data.setting]=data.value

            context["SETTING"]=setting_data

            context["MONEY_DATA"]=f"{setting_data['currency_symbol']},{setting_data['currency_decimal']}"



        except:
            T_setting=''

        master,create=Master_Setting.objects.get_or_create(setting="master_id")

        context["COMPANY_LIST"]=COMPANY_LIST
        context["COMPANY"]=CURRENT_COMPANY
        context["TODAY"]=timezone.localtime().strftime ("%d/%m/%Y")
        context["TODAY_PLAIN"] =timezone.localtime()
        context["CLIENT"]=master.value

        #print(context)

        return context
    else:
        return {}




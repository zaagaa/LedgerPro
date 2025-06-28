from setting.models import Setting
import json

def install_setting(company_id, setting, value):
    if not Setting.objects.filter(setting=setting, company_id=company_id).exists():
        Setting.objects.create(setting=setting, value=value, company_id=company_id)
    return Setting.objects.get(setting=setting, company_id=company_id).value

def default_setting_install(company_id):

    install_setting(company_id, "pos_header", 'COMPANY_NAME')
    install_setting(company_id, "pos_footer", '<div align="center">THANK YOU! VISIT AGAIN!</div>')
    install_setting(company_id, "pos_windows_header", '''**H1**{company.company_name}
**H3**A COMPLETE FAMILY SHOWROOM
No.101, Market Street
PH: 9999999999 
GST NAME: {company.company_name}
GST NO  : {company.tax_number}''')
    install_setting(company_id, "pos_windows_footer", 'THANK YOU! VISIT AGAIN!')
    install_setting(company_id, "pos_windows_show_tax", 'Enable')
    install_setting(company_id, "attendance_finish", '')


def install_global_settings():
    install_setting(None, "auto_screen_lock", 'Disable')
    install_setting(None, "auto_screen_lock_time", '30')
    install_setting(None, "price_code", json.dumps(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]))
    install_setting(None, "barcode_method", "{YEAR}A{ID}")
    install_setting(None, "currency_denomination", '2000;500;200;100;50;20;10;5;2;1')
    install_setting(None, "bundle_transport", 'BLUEDART;DHL;AKR;RATHIMEENA;METTUR;')
    install_setting(None, "currency_symbol", '₹')
    install_setting(None, "currency_decimal", '2')
    install_setting(None, "pos_round_off", "60")
    install_setting(None, "staff_api_url", "")
    install_setting(None, "early_comer_incentive", "50")

    install_setting(None, "customer_point_amount", "100")
    install_setting(None, "customer_min_deduction", "100")
    install_setting(None, "customer_inactive_days", "365")
    # install_setting(None, "online_database_url", "")

    install_setting(None, "monthly_leave_per_staff", "4")
    install_setting(None, "daily_leave_all_staff", "4")
    install_setting(None, "staff_approved_leave_incentive", "200")
    install_setting(None, "staff_unapproved_leave_penalty", "200")
    install_setting(None, "staff_leave_incentive_system", "Disable")
    install_setting(None, "staff_leave_booking_at_a_time", "2")
    install_setting(None, "staff_max_booking_period", "60")

    install_setting(None, "app_sale_report_mobile_numbers", "")



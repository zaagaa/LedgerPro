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
    install_setting(None, "staff_entry_time", "9:00 AM")
    install_setting(None, "staff_exit_time", "9:15 PM")
    install_setting(None, "staff_late_entry_time", "9:30 AM")
    install_setting(None, "staff_early_exit_time", "8:15 PM")
    install_setting(None, "staff_monthly_holiday", "4")

    install_setting(None, "app_sale_report_mobile_numbers", "")

    # ✅ AWS S3 Default Settings
    install_setting(None, "AWS_ACCESS_KEY_ID", "")
    install_setting(None, "AWS_SECRET_ACCESS_KEY", "")
    install_setting(None, "AWS_STORAGE_BUCKET_NAME", "")
    install_setting(None, "AWS_S3_REGION_NAME", "ap-south-1")  # default to Mumbai

    install_setting(None, "sms_alert_provider", "smsintegra.net")
    install_setting(None, "sms_alert_username", "")
    install_setting(None, "sms_alert_password", "")
    install_setting(None, "sms_alert_sid", "")
    install_setting(None, "sms_alert_entityid", "")

    install_setting(None, "sms_template_id_point_deduction", "1607100000000021554")
    install_setting(None, "sms_template_content_point_deduction",
                    "Hello {customer_name}, You Request a Gift for {deducted_point} Points. After the Gift your Balance Point is {balance_point} Points, Thank you for Shopping . OTP: {otp}")

    install_setting(None, "sms_template_id_point_added", "1607100000000021556")
    install_setting(None, "sms_template_content_point_added",
                    "Hello {customer_name}, Invoice No.{invoice_no} Your Current Purchase Point is: {point}, Your Total Points: {current_point}, Thank You for Shopping.")

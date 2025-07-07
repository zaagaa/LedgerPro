from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def setup_default_settings(sender, **kwargs):
    if sender.name == 'setting':  # Only run when the 'setting' app is migrated
        from company.models import Company
        from setting.utils import default_setting_install, install_global_settings

        for company in Company.objects.all():
            default_setting_install(company.id)

        install_global_settings()

        print("Setting Installed Successfully!")

# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# import os
#
# @receiver(post_migrate)
# def setup_default_settings(sender, **kwargs):
#     # Skip if DATABASE_URL is set (i.e. online)
#     if os.getenv('DATABASE_URL'):
#         print("⏭️ Skipping default setting install: ONLINE DATABASE detected.")
#         return
#
#     if sender.name == 'setting':
#         from company.models import Company
#         from setting.utils import default_setting_install, install_global_settings
#
#         for company in Company.objects.all():
#             default_setting_install(company.id)
#
#         install_global_settings()
#
#         print("✅ Default settings installed on OFFLINE database.")

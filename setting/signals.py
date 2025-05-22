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

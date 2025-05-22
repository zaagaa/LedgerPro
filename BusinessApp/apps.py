from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BusinessApp'

    def ready(self):
        from django.db import connection

        try:
            # Only run if the Setting table is ready
            if 'setting_setting' in connection.introspection.table_names():
                # ✅ Import models and utility safely inside ready()
                from company.models import Company
                from setting.utils import default_setting_install, install_setting, install_global_settings

                # ✅ Install settings per company
                for company in Company.objects.all():
                    default_setting_install(company.id)

                # ✅ Install global setting
                install_global_settings()

        except (OperationalError, ProgrammingError):
            # Happens during migrate or initial setup
            pass

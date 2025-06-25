from django.apps import AppConfig


class SyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sync'

    def ready(self):
        import sync.signals  # connects the signal on app ready

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.apps import apps

from sync.utils import log_deleted_instance

# Avoid logging system model deletions (or your own log table)
EXCLUDE_APPS = {'admin', 'auth', 'contenttypes', 'sessions', 'sync'}

@receiver(pre_delete)
def log_all_deletions(sender, instance, **kwargs):
    if sender._meta.app_label in EXCLUDE_APPS:
        return
    try:
        log_deleted_instance(instance)
    except Exception as e:
        print(f"❌ Failed to log deletion of {sender.__name__}({instance.pk}): {e}")

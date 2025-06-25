import time
from django.db.models.signals import pre_save
from django.dispatch import receiver

def current_unix_ms():
    return int(time.time() * 1000)


from django.conf import settings

print("yes")

@receiver(pre_save)
def update_sync_unix_globally(sender, instance, **kwargs):
    if sender._meta.app_label in ['admin', 'auth', 'contenttypes', 'sessions']:
        return

    now_ms = current_unix_ms()
    if hasattr(instance, 'sync_offline') and settings.INSTANCE_TYPE == 'offline':
        instance.sync_offline = now_ms

    if hasattr(instance, 'sync_online') and settings.INSTANCE_TYPE == 'online':
        instance.sync_online = now_ms

    print(f"Updating sync field for {sender.__name__} | Mode: {settings.INSTANCE_TYPE}")
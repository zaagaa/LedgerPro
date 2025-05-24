from django.db import models
from django.conf import settings
from django.utils.timesince import timesince

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    icon = models.CharField(max_length=50, default='bell')  # Optional: "bell", "check", "alert"
    image = models.ImageField(upload_to='notifications/', null=True, blank=True)
    url = models.URLField(default='#')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def time_ago(self):
        return timesince(self.created_at) + ' ago'

    def __str__(self):
        return f"{self.user} - {self.message[:30]}"
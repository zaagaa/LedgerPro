from django import template
from django.utils import timezone
from datetime import datetime, timedelta
register = template.Library()

@register.filter
def pluck(value, key):
    return [v.get(key, '') for v in value]

@register.filter
def days_ago(days, date_format="%d/%m/%Y"):
    try:
        return (timezone.localtime() - timedelta(days=int(days))).strftime(date_format)
    except:
        return ""
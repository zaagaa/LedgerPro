from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def querystring_without(request, *exclude_keys):
    query = request.GET.copy()
    for key in exclude_keys:
        query.pop(key, None)
    return query.urlencode()

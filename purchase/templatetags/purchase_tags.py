from django import template


register = template.Library()


@register.filter
def get_nested_attr(obj, attr_str):
    attrs = attr_str.split('.')
    for attr in attrs:
        obj = getattr(obj, attr, '')
        if callable(obj):
            obj = obj()
    return obj


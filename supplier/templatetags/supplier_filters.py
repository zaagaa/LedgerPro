from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if not dictionary:
        return 0

    return dictionary.get(key, 0)


@register.filter
def indian_number(value):

    try:
        value = float(value)
    except (ValueError, TypeError):
        return "0.00"

    return f"{value:,.2f}"
# statement/templatetags/cash_tags.py

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@register.simple_tag
def cumulative_total(denomination_list):
    total = 0
    for item in denomination_list:
        for denom, qty in item.items():
            total += int(denom) * int(qty)
    return total

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        if isinstance(dictionary, dict):
            return dictionary.get(int(key))
        else:
            return None
    except:
        return None

@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except:
        return ""


@register.filter
def get_total(section_dict, key):
    """
    Calculates the sum of a specific key across all section dictionaries.
    Usage: {{ sections|get_total:"total" }}
    """
    try:
        return sum(float(section.get(key, 0)) for section in section_dict.values())
    except Exception:
        return 0


@register.filter
def sum_field(queryset, field):
    total = 0
    for item in queryset:
        try:
            total += float(getattr(item, field, 0) or 0)
        except (ValueError, TypeError):
            continue
    return total
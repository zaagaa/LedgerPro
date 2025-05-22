from django import template
from datetime import datetime

register = template.Library()

@register.filter
def unix_to_time(value):
    try:
        return datetime.fromtimestamp(int(value)).strftime("%I:%M:%S %p")
    except:
        return "-"

@register.filter
def intcomma_indian(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value

    is_negative = value < 0
    value = abs(value)

    number = str(int(value))
    if len(number) <= 3:
        result = number
    else:
        last3 = number[-3:]
        rest = number[:-3]
        rest_with_commas = ','.join(
            [rest[max(i - 2, 0):i] for i in range(len(rest), 0, -2)][::-1]
        )
        result = rest_with_commas + ',' + last3

    decimal_part = f"{value:.2f}".split('.')[-1]
    formatted = f"{result}.{decimal_part}"

    return f"-{formatted}" if is_negative else formatted

@register.filter
def extract_list(values, index):
    try:
        index = int(index)
        return [v[index] for v in values if isinstance(v, (list, tuple))]
    except Exception:
        return []

@register.filter
def pluck(value, key):
    return [v.get(key, '') for v in value]



@register.filter
def dict_items(value):
    try:
        return value.items()
    except:
        return []


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



@register.filter
def get_month_name(month_number):
    import calendar
    return calendar.month_name[int(month_number)]

@register.filter
def to_range(start, end):
    return range(start, end + 1)

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except:
        return ''

@register.filter
def sum_list(lst):
    return round(sum(lst), 2) if lst else 0


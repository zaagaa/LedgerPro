from django import template

register = template.Library()

@register.filter
def visible_duration_human(ms):
    try:
        ms = int(ms or 0)
        if ms < 1000:
            return "-"
        minutes, seconds = divmod(ms // 1000, 60)
        if minutes > 0:
            return f"{minutes} min {seconds} sec"
        return f"{seconds} sec"
    except:
        return "-"

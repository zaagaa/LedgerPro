from django import template

from setting.models import Setting
from decimal import Decimal

register=template.Library()

class TestTagNode(template.Node):
    def render(self, context):
        return context['request'].user

@register.filter(name='subtract')
def subtract(a,b):
    if a is None:
        a=0
    if b is None:
        b=0
    return float(a) - float(b)

@register.filter(name='addition')
def addition(a,b):
    if a is None:
        a=0
    if b is None:
        b=0
    return float(a) + float(b)

@register.filter(name='multiply')
def multiply(a,b):
    if a is None or a=='':
        a=0
    if b is None or b=='':
        b=0
    return float(a) * float(b)

@register.filter(name='cheque')
def cheque(a):
    if a is None or a=='':
        a="-"
    else:
        a=int(a)
        a=f"{a :06d}"

    return a





# def _formatted_len(s: float, decimals: int = 2, sign: str = "-"):
#     formatted_s = f"{s:{sign},.{decimals}f}"
#     return len(formatted_s)
#
# def currency(x: float, symbol: str = "$", decimals: int = 2, sign: str  = "-"):
#     assert len(symbol) == 1
#     assert sign in ["-", "+", " "]
#     length = _formatted_len(x, decimals, sign)
#     # return length
#     x=special_format(x)
#     return f"{x:.{decimals}f}"
# # return f"{x:{symbol}={sign}{length + 1},.{decimals}f}"
# return currency(a, symbol="₹", decimals=3, sign="-")



def special_format(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)


def user(request):
    return request.user.username




@register.filter(name='money')
def money(a, MONEY_DATA):
    """
    Usage: {{ amount|money:"₹,2" }}
    """
    try:
        currency = MONEY_DATA.split(",")

        if len(currency) != 2:
            return f"{a}"  # Or return empty, or raise error, based on your choice

        symbol = currency[0]
        decimals = int(currency[1])

        if a is None or a == '':
            return None

        a = Decimal(a)
        formatted = f"{a:.{decimals}f}"

        return f"{symbol}{special_format(formatted)}"

    except Exception as e:
        # Optional: log this error or return fallback
        return str(a)
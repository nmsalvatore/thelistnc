from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def remove_periods(val):
    return val.replace(".", "")

@register.filter
@stringfilter
def contains(val, arg):
    return str(arg in val).lower()

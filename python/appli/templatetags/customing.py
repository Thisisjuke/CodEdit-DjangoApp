from django import template

register = template.Library()

@register.simple_tag()
def multiply(unit, *args):
    indent = '&emsp;' * int(unit)
    return indent

from django import template

register = template.Library()

@register.simple_tag()
def multiply(unit, *args):
    indent = '&emsp;' * int(unit)
    return indent

@register.filter(name='addclass')
def addclass(value, arg):
    css_classes = value.field.widget.attrs.get('class', '').split(' ')
    if css_classes and arg not in css_classes:
        css_classes = '%s %s' % (css_classes, arg)
    return value.as_widget(attrs={'class': css_classes})

@register.filter(name='addplaceholder')
def addplaceholder(value, arg):
    return value.as_widget(attrs={'placeholder': arg})
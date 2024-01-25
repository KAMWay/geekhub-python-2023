from django import template

register = template.Library()


@register.filter(name='inside')
def inside(value, items):
    for item in items:
        if value in item.values():
            return True
    return False

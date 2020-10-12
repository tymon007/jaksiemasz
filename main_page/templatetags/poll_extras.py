from django import template

register = template.Library()


@register.filter
def addition(val1, val2):
    return int(val1) + int(val2)


@register.filter
def subtraction(val1, val2):
    return int(val1) - int(val2)


@register.filter
def multiplication(val1, val2):
    return int(val1) * int(val2)


@register.filter
def division(val1, val2):
    return int(val1) / int(val2)


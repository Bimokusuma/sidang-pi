from django import template

register = template.Library()

@register.filter
def index(idxable, i):
    return idxable[i]

from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def addDays(d, days):
    newDate = d + timedelta(days=int(days))
    return newDate


@register.filter
def getImages(mememoitem):
    return mememoitem.getImage()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context["request"].GET.copy()
    query.update(kwargs)
    return query.urlencode()


@register.simple_tag(takes_context=True)
def url_replacex(context, **kwargs):
    query = context["request"].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

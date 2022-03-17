from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='addDays')
def addDays(d, days):
   newDate = d + timedelta(days=days)
   return newDate

@register.filter
def getImages(mememoitem):
   return mememoitem.getImage()

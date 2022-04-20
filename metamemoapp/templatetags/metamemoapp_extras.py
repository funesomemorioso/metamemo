from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def addDays(d, days):
   newDate = d + timedelta(days=int(days))
   return newDate

@register.filter
def getImages(mememoitem):
   return mememoitem.getImage()

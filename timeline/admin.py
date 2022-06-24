from django.contrib import admin

from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget

from timeline.models import Fact, Timeline, Session

# Register your models here.

class FactAdmin(ImportExportModelAdmin):
    model = Fact
    list_display = ('date', 'text', 'timeline','source')
    list_filter = ('timeline__name', 'date')

class SessionAdmin(ImportExportModelAdmin):
    model = Session
    list_display = ('start','end','timeline','text')


class TimelineAdmin(ImportExportModelAdmin):
    model = Timeline
    list_display = ('start', 'end','name')

admin.site.register(Fact, FactAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Timeline, TimelineAdmin)

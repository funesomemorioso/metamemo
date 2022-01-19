from django.contrib import admin

# Register your models here.
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MemoMedia


class MemoItemAdmin(admin.ModelAdmin):
    model = MemoItem
    list_display = ('title', 'author','content_date', 'source')

admin.site.register(MetaMemo)
admin.site.register(MemoItem, MemoItemAdmin)
admin.site.register(MemoSource)
admin.site.register(MemoMedia)
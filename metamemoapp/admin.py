from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html


import shlex
# Register your models here.
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MemoMedia

from metamemoapp.tasks import transcribe_async, download_async

"""
Esse é o principal motivo pelo qual eu quis vir pro django.
Com poucas linhas a gente tem uma interface administrativa robusta e customizável.

O list_display mostra quais campos exibir na interface administrativa.
Tem outros parametros para configurar filtros, facets e coisas mais.
Vale ler a documentação.
"""


#Action para baixar as midias. TODO: Precisa jogar o job prum Celery da vida.
def download_media(modeladmin, request, queryset):
    for i in queryset.all():
        if i.status == 'INITIAL':
            download_async.delay(i.pk)
            i.status = 'QUEUED'
            i.save()
            messages.add_message(request, messages.SUCCESS, 'Download job started.')

download_media.short_description = 'Download Media'

def transcribe_media(modeladmin, request, queryset):
    for i in queryset.filter(status='DOWNLOADED'):
        transcribe_async.delay(i.pk)
        i.status = 'QUEUED'
        i.save()
        messages.add_message(request, messages.SUCCESS, 'Transcription job started.')
transcribe_media.short_description = 'Transcribe Media'



class MemoMediaAdmin(admin.ModelAdmin):
    model = MemoMedia
    list_display = ('original_url', 'status', 'mediatype')
    actions = [download_media, transcribe_media]

@admin.display(description='Link')
def link_to_memoitem(obj):
    return format_html(f'<a href="{obj.url}" target="_blank">🔗</a>')

class MemoItemAdmin(admin.ModelAdmin):
    model = MemoItem
    list_display = ('title', 'author','content_date', 'source', 'likes', 'interactions', 'shares', link_to_memoitem)
    list_filter = ('source__name', 'author__name')
    search_fields = ('content',)

    
admin.site.register(MetaMemo)
admin.site.register(MemoItem, MemoItemAdmin)
admin.site.register(MemoSource)
admin.site.register(MemoMedia, MemoMediaAdmin)
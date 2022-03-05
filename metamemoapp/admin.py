from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget

import shlex
# Register your models here.
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MemoMedia, MemoKeyWord, MemoContext, MemoNews

from metamemoapp.tasks import transcribe_async, download_async
from metamemoapp.utils import generate_keyword
"""
Esse é o principal motivo pelo qual eu quis vir pro django.
Com poucas linhas a gente tem uma interface administrativa robusta e customizável.

O list_display mostra quais campos exibir na interface administrativa.
Tem outros parametros para configurar filtros, facets e coisas mais.
Vale ler a documentação.
"""


#Action para baixar as midias. TODO: Precisa jogar o job prum Celery da vida.
def download_media(modeladmin, request, queryset):
    for i in queryset.filter(status='INITIAL', mediatype='VIDEO'):
        i.status = 'DOWNLOADING'
        i.save()
        download_async.delay(url=i.original_url, mediatype='VIDEO')
        messages.add_message(request, messages.SUCCESS, 'Download job started.')

download_media.short_description = 'Download Video Media'

def transcribe_media(modeladmin, request, queryset):
    for i in queryset.filter(status='DOWNLOADED', mediatype='VIDEO'):
        i.status = 'TRANSCRIBING'
        i.save()
        transcribe_async.delay(pk=i.pk)
        messages.add_message(request, messages.SUCCESS, 'Transcription job started.')
transcribe_media.short_description = 'Transcribe Video Media'


def save_keywords(modeladmin, request, queryset):
    for i in queryset:
        text = i.content
        for m in i.medias.all():
            if m.transcription:
                text += m.transcription
        keywords = generate_keyword(text)
        for word,rank in keywords:
            w =  MemoKeyWord.objects.get_or_create(word=word)
            i.keyword.add(w[0])

class MemoMediaAdmin(admin.ModelAdmin):
    model = MemoMedia
    list_display = ('original_url', 'status', 'mediatype')
    actions = [download_media, transcribe_media]
    list_filter = ('mediatype', 'status')


@admin.display(description='Link')
def link_to_memoitem(obj):
    slug = '🔗'
    if isinstance(obj, MemoContext):
        slug = obj.source
    return format_html(f'<a href="{obj.url}" target="_blank">{slug}</a>')

@admin.display(description='Keywords')
def get_keywords(obj):
    if obj.keyword.all():
        return ", ".join([p.word for p in obj.keyword.all()])
    else:
        v = obj.medias.filter(mediatype='VIDEO').first()
        if v:
            return v.status

class MemoItemAdmin(admin.ModelAdmin):
    model = MemoItem
    list_display = ('title', 'author','content_date', 'source', 'likes', 'interactions', 'shares', get_keywords, link_to_memoitem)
    list_filter = ('source__name', 'author__name')
    search_fields = ('content',)
    actions = [save_keywords]

@admin.display(description="Posts")
def itens_in_context(obj):
    if obj.start_date and obj.end_date:
        return(MemoItem.objects.filter(content_date__gte=obj.start_date, content_date__lte=obj.end_date).count())


class MemoContextResource(resources.ModelResource):
    keyword=fields.Field(attribute='keyword', widget=ManyToManyWidget(MemoKeyWord, field='word'), column_name='keyword')
    
    class Meta:
        model = MemoContext
        fields = ('context', 'start_date', 'end_date', 'url', 'source', 'keyword')
        exclude = ('id',)
        import_id_fields = ('url','context')
        export_order = fields

class MemoContextAdmin(ImportExportModelAdmin):
    model = MemoContext
    resource_class = MemoContextResource
    filter_horizontal = ('keyword',)
    list_display = ('context','start_date','end_date', link_to_memoitem, itens_in_context,)


class MemoNewsAdmin(admin.ModelAdmin):
    model = MemoNews
    list_display = ('title', 'source', 'content_date', link_to_memoitem)

admin.site.register(MetaMemo)
admin.site.register(MemoItem, MemoItemAdmin)
admin.site.register(MemoSource)
admin.site.register(MemoMedia, MemoMediaAdmin)
admin.site.register(MemoKeyWord)
admin.site.register(MemoContext, MemoContextAdmin)
admin.site.register(MemoNews, MemoNewsAdmin)
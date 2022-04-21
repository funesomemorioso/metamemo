from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.db.models import Count

from import_export import resources,fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget

import shlex
# Register your models here.
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MemoMedia, MemoKeyWord, MemoContext, NewsItem
from metamemoapp.models import NewsCover, NewsSource
from metamemoapp.tasks import transcribe_async, download_async
from metamemoapp.utils import generate_keyword


"""
Esse é o principal motivo pelo qual eu quis vir pro django.
Com poucas linhas a gente tem uma interface administrativa robusta e customizável.

O list_display mostra quais campos exibir na interface administrativa.
Tem outros parametros para configurar filtros, facets e coisas mais.
Vale ler a documentação.
"""


#Action para baixar as midias.
def download_media(modeladmin, request, queryset):
    if queryset.model is MemoMedia:
        for i in queryset:
            if i.mediatype == 'VIDEO':
                i.status = 'DOWNLOADING'
                i.save()
                download_async.apply_async(kwargs={'url': i.original_url, 'mediatype': 'VIDEO'})
                messages.add_message(request, messages.SUCCESS, 'Download job started.')
    elif queryset.model is MemoItem:
        for i in queryset:
            for v in i.medias:
                if v.mediatype == 'VIDEO':
                    v.status = 'DOWNLOADING'
                    v.save()
                    download_async.apply_async(kwargs={'url': v.original_url, 'mediatype': 'VIDEO'})
                    messages.add_message(request, messages.SUCCESS, 'Download job started.')

download_media.short_description = 'Download Video Media'

def transcribe_media(modeladmin, request, queryset):
    if queryset.model is MemoMedia:
        for i in queryset.filter(status='DOWNLOADED', mediatype='VIDEO'):
            i.status = 'TRANSCRIBING'
            i.save()
            transcribe_async.apply_async(kwargs={'url': i.original_url, 'mediatype': 'VIDEO'})
            messages.add_message(request, messages.SUCCESS, 'Transcription job started.')
    elif queryset.model is MemoItem:
        for i in queryset.filter(medias__status='DOWNLOADED', medias__mediatype='VIDEO'):
            for v in i.medias.filter(mediatype='VIDEO'):
                v.status = 'TRANSCRIBING'
                v.save()
                transcribe_async.apply_async(kwargs={'url': v.original_url, 'mediatype': 'VIDEO'})
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
    if obj.keyword:
        return ", ".join([p.word for p in obj.keyword.all()])
    else:
        return ""

@admin.display(description='Status')
def video_status(obj):
    for v in obj.medias.all():
        if v.mediatype=='VIDEO':
            if v.status == 'DOWNLOADING':
                return f'{v.status} ({v.progress})'
            return v.status
    
class MemoItemAdmin(ImportExportModelAdmin):
    model = MemoItem
    list_display = ('title', 'author','content_date', 'source', 'likes', 'interactions', 'shares', get_keywords, video_status, link_to_memoitem)
    list_filter = ('source__name', 'author__name', 'medias__status', 'medias__mediatype')
    raw_id_fields = ('medias',)
    search_fields = ('content',)
    filter_horizontal = ('keyword',)
    readonly_fields = ('raw',)
    actions = [download_media, transcribe_media, save_keywords]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('medias').prefetch_related('keyword')

    
    
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


class NewsItemAdmin(admin.ModelAdmin):
    model = NewsItem
    list_display = ('title', 'source', 'content_date', link_to_memoitem)


class MemoKeyWordAdmin(admin.ModelAdmin):
    model = MemoKeyWord
    list_display = ('word', 'word_count')

    def word_count(self, obj):
        return obj.word_count
    
    word_count.admin_order_field = 'word_count'


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(word_count=Count("memoitem"))
        return queryset



#Resources

class MemoItemResource(resources.ModelResource):
    class Meta:
        model = MemoItem
        fields = ('original_id', 'content_date', 'author__name', 'source__name', 'title', 'content', 'likes', 'interactions', 'shares', 'url')


admin.site.register(MetaMemo)
admin.site.register(MemoItem, MemoItemAdmin)
admin.site.register(MemoSource)
admin.site.register(MemoMedia, MemoMediaAdmin)
admin.site.register(MemoKeyWord, MemoKeyWordAdmin)
admin.site.register(MemoContext, MemoContextAdmin)

admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsSource)
admin.site.register(NewsCover)
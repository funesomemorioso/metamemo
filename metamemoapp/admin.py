from django.contrib import admin
from django.core.management import call_command
import shlex
# Register your models here.
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MemoMedia, MetaScraper

from metamemoapp.tasks import transcribe_async

"""
Esse é o principal motivo pelo qual eu quis vir pro django.
Com poucas linhas a gente tem uma interface administrativa robusta e customizável.

O list_display mostra quais campos exibir na interface administrativa.
Tem outros parametros para configurar filtros, facets e coisas mais.
Vale ler a documentação.
"""

def run_scraper(modeladmin, request, queryset):
        for scraper in queryset:
            call_command(scraper.command, *shlex.split(scraper.command_args))

run_scraper.short_description = 'Run scraper'

#Action para baixar as midias. TODO: Precisa jogar o job prum Celery da vida.
def download_media(modeladmin, request, queryset):
    for i in queryset.all():
        if i.status == 'INITIAL':
            i.download_media()

download_media.short_description = 'Download Media'

def transcribe_media(modeladmin, request, queryset):
    for i in queryset.all():
        if i.status == 'DOWNLOADED':
            transcribe_async.delay(i.pk)

transcribe_media.short_description = 'Transcribe Media'



class MemoMediaAdmin(admin.ModelAdmin):
    model = MemoMedia
    list_display = ('original_url', 'status')
    actions = [download_media, transcribe_media]

class MemoItemAdmin(admin.ModelAdmin):
    model = MemoItem
    list_display = ('title', 'author','content_date', 'source', 'likes')
    list_filter = ('source__name', 'author__name')
    search_fields = ('content',)

# TODO: Trocar para um sistema de agendamento de tarefas

class MetaScraperAdmin(admin.ModelAdmin):
    model = MetaScraper
    list_display = ('source', 'url', 'command')
    actions = [run_scraper,]
    
admin.site.register(MetaMemo)
admin.site.register(MetaScraper, MetaScraperAdmin)
admin.site.register(MemoItem, MemoItemAdmin)
admin.site.register(MemoSource)
admin.site.register(MemoMedia, MemoMediaAdmin)
from django.contrib import admin
from django.core.management import call_command
import shlex
# Register your models here.
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MemoMedia, MetaScraper

"""
Esse é o principal motivo pelo qual eu quis vir pro django.
Com poucas linhas a gente tem uma interface administrativa robusta e customizável.

O list_display mostra quais campos exibir na interface administrativa.
Tem outros parametros para configurar filtros, facets e coisas mais.
Vale ler a documentação.
"""

class MemoItemAdmin(admin.ModelAdmin):
    model = MemoItem
    list_display = ('title', 'author','content_date', 'source', 'likes')
    list_filter = ('source__name', 'author__name')
    search_fields = ('content',)

# TODO: Trocar para um sistema de agendamento de tarefas

def run_scraper(modeladmin, request, queryset):
    for scraper in queryset:
        call_command(scraper.command, *shlex.split(scraper.command_args))

run_scraper.short_description = 'Run scraper'


class MetaScraperAdmin(admin.ModelAdmin):
    model = MetaScraper
    list_display = ('source', 'url', 'command')
    actions = [run_scraper,]
    
admin.site.register(MetaMemo)
admin.site.register(MetaScraper, MetaScraperAdmin)
admin.site.register(MemoItem, MemoItemAdmin)
admin.site.register(MemoSource)
admin.site.register(MemoMedia)
from django.contrib import admin

# Register your models here.
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MemoMedia

"""
Esse é o principal motivo pelo qual eu quis vir pro django.
Com poucas linhas a gente tem uma interface administrativa robusta e customizável.

O list_display mostra quais campos exibir na interface administrativa.
Tem outros parametros para configurar filtros, facets e coisas mais.
Vale ler a documentação.
"""

class MemoItemAdmin(admin.ModelAdmin):
    model = MemoItem
    list_display = ('title', 'author','content_date', 'source')

admin.site.register(MetaMemo)
admin.site.register(MemoItem, MemoItemAdmin)
admin.site.register(MemoSource)
admin.site.register(MemoMedia)
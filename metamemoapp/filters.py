import django_filters
from metamemoapp.models import MemoItem, MemoNews, MetaMemo, MemoSource
from django.template.defaulttags import register

class MemoItemFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains') #speedup?
    start_date = django_filters.DateFilter(field_name='content_date',lookup_expr=('gte')) 
    end_date = django_filters.DateFilter(field_name='content_date',lookup_expr=('lte'))
    author= django_filters.ModelMultipleChoiceFilter(field_name='author__name', to_field_name='name', queryset=MetaMemo.objects.all())
    source = django_filters.ModelMultipleChoiceFilter(field_name='source__name', to_field_name='name', queryset=MemoSource.objects.all())
    
    class Meta:
        model = MemoItem
        fields = ['author__name', 'source__name']


class MemoNewsFilter(django_filters.FilterSet):
    author__name = django_filters.CharFilter(field_name='metamemo__name', lookup_expr='exact')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
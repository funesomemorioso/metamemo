import django_filters
from metamemoapp.models import MemoItem, MemoNews

class MemoItemFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains') #speedup?
    class Meta:
        model = MemoItem
        fields = ['author__name', 'source__name']


class MemoNewsFilter(django_filters.FilterSet):
    author__name = django_filters.CharFilter(field_name='metamemo__name', lookup_expr='exact')
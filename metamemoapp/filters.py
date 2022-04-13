import django_filters
from metamemoapp.models import MemoItem, MemoNews

class MemoItemFilter(django_filters.FilterSet):
    date__start = django_filters.DateTimeFilter(field_name='content_date', lookup_expr='gte')
    date__end = django_filters.DateTimeFilter(field_name='content_date', lookup_expr='lte')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains') #speedup?
    class Meta:
        model = MemoItem
        fields = ['author__name', 'source__name']


class MemoNewsFilter(django_filters.FilterSet):
    date__start = django_filters.DateTimeFilter(field_name='content_date', lookup_expr='gte')
    date__end = django_filters.DateTimeFilter(field_name='content_date', lookup_expr='lte')

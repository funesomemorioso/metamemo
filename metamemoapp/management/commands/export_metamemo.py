from django.core.management.base import BaseCommand

from metamemoapp.admin import MemoItemResource
from metamemoapp.models import MemoItem


class Command(BaseCommand):
    help = 'Export database'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--author', type=str, help='Metamemos to include')
        parser.add_argument('-s', '--source', type=str, help='Metamemos to include')
        parser.add_argument('-n', '--number', type=int, help='Limit by number')

    def handle(self, *args, **kwargs):
        self.author = kwargs['author']
        self.source = kwargs['source']
        self.number = kwargs['number']
        
        queryset = MemoItem.objects.all()
        queryset = queryset.exclude(source__name='Blog') #Html cagando tudo
        if self.author:
            authors = self.author.split(",")
            queryset = queryset.filter(author__name__in=authors)
        if self.source:
            sources = self.source.split(",")
            queryset = queryset.filter(source__name__in=sources)
        
        if self.number:
            queryset = queryset[0:self.number]

        export = MemoItemResource().export(queryset)
        print(export.csv)

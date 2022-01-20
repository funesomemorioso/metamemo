from django.core.management.base import BaseCommand
from django.utils import timezone
from metamemoapp.models import MetaMemo, MemoItem, MemoSource
import csv
import json

"""
Cada arquivo dentro de management/commands é um comando que pode ser rodado usando 'python manage.py nomedocomando'.
Handle() é a função executada pelo código.
A vantagem de fazer assim é que as libs e dependencias do Django já estão encapsuladas e você pode chamar essa função dentro do resto do código.
"""

class Command(BaseCommand):
    help = 'Importa de um arquivo de facebook'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', type=str, help='CSV File to be imported')
        parser.add_argument('-a', '--author', type=str, help='MetaMemo Author Name')


    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        author = kwargs['author']
        
        memo_author = MetaMemo.objects.get_or_create(name=author)
        memo_source = MemoSource.objects.get_or_create(name='Facebook')
        input_file = csv.DictReader(open(filename, 'r'))
        
        """
        Aqui estou usando o MemoItem() para instancear um objeto que defini lá no models.
        E a função save() para salvar efetivamente no banco.
        Tem um outro jeito de fazer onde você comita todas as alterações e salva de uma vez, acho que vale refatorar depois.

        """
        
        for i in input_file:
            post = MemoItem()
            post.author = memo_author[0]
            post.source = memo_source[0]
            post.title = i['post_text'][0:139]
            post.content = i['post_text']
            post.extraction_date = '2022-01-20 00:00:00'
            post.content_date = i['time']
            post.url = i['post_url']
            post.likes = i['likes']
            post.interactions = i['comments']
            post.raw = json.dumps(i)
            post.save()
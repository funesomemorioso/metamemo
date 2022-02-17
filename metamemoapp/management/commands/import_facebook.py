from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from django.utils import timezone
from metamemoapp.models import MetaMemo, MemoItem, MemoSource
import json, pprint, os
import facebook_scraper

"""
Cada arquivo dentro de management/commands é um comando que pode ser rodado usando 'python manage.py nomedocomando'.
Handle() é a função executada pelo código.
A vantagem de fazer assim é que as libs e dependencias do Django já estão encapsuladas e você pode chamar essa função dentro do resto do código.
"""
    

class Command(BaseCommand):
    help = 'Importa de um arquivo de facebook'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help='Facebook Username')
        parser.add_argument('-a', '--author', type=str, help='MetaMemo Author Name')
        parser.add_argument('-c', '--clear', action='store_true')


    def handle(self, *args, **kwargs):
        username = kwargs['username']
        author = kwargs['author']
        clear = kwargs['clear']
        
        memo_author = MetaMemo.objects.get_or_create(name=author)
        memo_source = MemoSource.objects.get_or_create(name='Facebook')
        
    
        memo_itens = MemoItem.objects.filter(author__name=author, source__name='Facebook').values_list('original_id', flat=True)
        
        #Esvazia lista de ids caso passe a flag --clear;
        #TODO: Excluir os posts em caso de clear. Não fiz ainda para manter os posts p/ debug.
        if clear:
            memo_itens = []


        #Leva as configurações para o settings.py (que herdam do .env)
        cookies_file = getattr(settings, "FACEBOOK_COOKIES", None)
        pages = getattr(settings, "FACEBOOK_PAGES", 4)
        ppp = getattr(settings, "FACEBOOK_PPP", 10)
        
        if not cookies_file or not os.path.isfile(cookies_file):
            print("Facebook Cookie File not found!")
            raise 
        input_posts = facebook_scraper.get_posts(username, pages=pages, options={'posts_per_page':ppp, "allow_extra_requests": False}, cookies=cookies_file)
        
        """
        Aqui estou usando o MemoItem() para instancear um objeto que defini lá no models.
        E a função save() para salvar efetivamente no banco.
        Tem um outro jeito de fazer onde você comita todas as alterações e salva de uma vez, acho que vale refatorar depois.

        """
        
        for i in input_posts:
            if i['post_id'] in memo_itens:
                print("Done!")
                break
            else:
                pprint.pprint(i, indent=3)
                post = MemoItem()
                post.author = memo_author[0]
                post.source = memo_source[0]
                if i['text']:
                    post.title = i['text'][0:139].replace('\n',' ')
                else:
                    post.title = "" #FIX
                post.content = i['post_text']
                post.extraction_date = '2022-01-20 00:00:00' #FIX
                post.content_date = i['time']
                post.url = i['post_url']
                post.likes = i['likes']
                post.shares = i['shares']
                post.interactions = i['comments']
                post.original_id = i['post_id']
                post.raw = json.dumps(i, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                post.save()

            #Cria um metaitem com status INITIAL caso existam vídeos        
                if i['video']:
                    post.medias.create(original_url=f"http://facebook.com/{i['video_id']}", original_id=i['video_id'], status='INITIAL')

        
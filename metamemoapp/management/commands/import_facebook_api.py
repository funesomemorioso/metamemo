from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from django.utils import timezone
from metamemoapp.models import MetaMemo, MemoItem, MemoSource
import json, pprint, os, datetime
import urllib

class Command(BaseCommand):
    help = 'Importa de um arquivo de facebook via Crowdtangle'

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
        apikey = getattr(settings, 'CROWDTANGLE_API_KEY', None)
        pages = getattr(settings, 'CROWDTANGLE_POSTS_COUNT', 10)
        interval = urllib.parse.quote_plus(getattr(settings, 'CROWDTANGLE_POSTS_INTERVAL', '90 DAY'))
        
        url = f'https://api.crowdtangle.com/posts?token={apikey}&accounts={username}&sortBy=date&timeframe={interval}'
        
        response = urllib.request.urlopen(url)
        input_posts = json.load(response)

        
        if input_posts['status'] == 200:
            for i in input_posts['result']['posts']:
                post_id = int(i['id'].split('|')[1])
                if post_id in memo_itens:
                    print("Done!")
                    break
                else:
                    post = MemoItem()
                    post.author = memo_author[0]
                    post.source = memo_source[0]
                    if i['message']:
                        post.title = i['message'][0:139].replace('\n',' ')
                    else:
                        post.title = "" #FIX
                    post.content = i['message']
                    post.extraction_date = datetime.datetime.now()
                    post.content_date = i['date']
                    post.url = i['postUrl']
                    post.likes = i['statistics']['actual']['likeCount']
                    post.shares = i['statistics']['actual']['shareCount']
                    post.interactions = i['statistics']['actual']['commentCount']
                    post.original_id = post_id
                    post.raw = json.dumps(i, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                    print(post)
                    post.save()

                #Cria um metaitem com status INITIAL caso existam vídeos
                    if i['type'] in ['live_video_complete', 'native_video']:
                        post.medias.create(original_url=i['link'], original_id=post_id, status='INITIAL')

        
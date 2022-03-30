from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from django.utils import timezone
from metamemoapp.models import MetaMemo, MemoItem, MemoSource
import json, pprint, os, datetime
import tweepy
from decouple import config
from textwrap import shorten
from metamemoapp.tasks import download_img_async, download_async


TITLE_MAX_CHAR = 300

"""
Cada arquivo dentro de management/commands é um comando que pode ser rodado usando 'python manage.py nomedocomando'.
Handle() é a função executada pelo código.
A vantagem de fazer assim é que as libs e dependencias do Django já estão encapsuladas e você pode chamar essa função dentro do resto do código.
"""
    

class Command(BaseCommand):
    help = 'Importa de um usuário do twitter'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help='Twitter Username')
        parser.add_argument('-a', '--author', type=str, help='MetaMemo Author Name')
        parser.add_argument('-m', '--media', action='store_true')


    def handle(self, *args, **kwargs):
        self.username = kwargs['username']
        self.author = kwargs['author']
        self.video_download = kwargs['media']

        self.memo_author = MetaMemo.objects.get_or_create(name=self.author)
        self.memo_source = MemoSource.objects.get_or_create(name='Twitter')
        
    
        self.memo_itens = MemoItem.objects.filter(author__name=self.author, source__name='Twitter').values_list('original_id', flat=True)
        
        self.twitter_bearer = config('TWITTER_BEARER_TOKEN', default='')
        
        if not self.twitter_bearer:
            print("You need to setup the bearer token in .env")
            raise 
        
        self.client = tweepy.Client(self.twitter_bearer)
        self.user = self.client.get_user(username=self.username)
        
        self.getTweets()

    def getTweets(self, paginationToken=None):
        input_posts = self.client.get_users_tweets(self.user.data.id, media_fields=["url","type","media_key"], expansions="attachments.media_keys",  tweet_fields="created_at,public_metrics", max_results=100, pagination_token=paginationToken)
        
        """
        Aqui estou usando o MemoItem() para instancear um objeto que defini lá no models.
        E a função save() para salvar efetivamente no banco.
        Tem um outro jeito de fazer onde você comita todas as alterações e salva de uma vez, acho que vale refatorar depois.

        """
        
        tweet_media = {}
        
        if 'media' in input_posts.includes:
            for m in input_posts.includes['media']:
                if m['type'] == 'video':
                    tweet_media[m['media_key']] = 'VIDEO'
                elif m['type'] == 'photo':
                    tweet_media[m['media_key']] = 'IMAGE'
                else:
                    pass

        for i in input_posts.data:
            if i.id in self.memo_itens:
                print("Done!")
                break
            else:
                pprint.pprint(i, indent=3)
                post = MemoItem()
                post.author = self.memo_author[0]
                post.source = self.memo_source[0]
                post.title = shorten(i.text, TITLE_MAX_CHAR)
                post.content = i.text
                post.extraction_date = datetime.datetime.now()
                post.content_date = i.created_at
                post.url = f'https://twitter.com/{self.user.data.username}/status/{i.id}'
                post.likes = i.public_metrics['like_count']
                post.shares = i.public_metrics['retweet_count']
                post.interactions = i.public_metrics['reply_count']
                post.original_id = i.id
                post.raw = json.dumps(dict(i), sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                post.save()

            #Cria um metaitem com status INITIAL caso existam vídeos        
                if i.attachments:
                    for m in i.attachments['media_keys']:
                        print(m)
                        p = post.medias.create(original_url=f'https://twitter.com/{self.user.data.username}/status/{i.id}', original_id=m, status='INITIAL', mediatype=tweet_media[m])
                        if p.mediatype=='VIDEO' and self.video_download:
                            p.status = 'DOWNLOADING'
                            p.save()
                            post.save()
                            download_async.apply_async(kwargs={'url': p.original_url, 'mediatype': 'VIDEO'})


                if 'next_token' in input_posts.meta:
                    self.getTweets(paginationToken=input_posts.meta['next_token'])

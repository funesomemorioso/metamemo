from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from django.utils import timezone
from metamemoapp.models import MetaMemo, MemoItem, MemoSource
import json, pprint, os, datetime
import urllib
from textwrap import shorten

from metamemoapp.tasks import download_img_async

TITLE_MAX_CHAR = 300

class Command(BaseCommand):
    help = 'Importa de um canal no Youtube'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--channel', type=str, help='Channel Id')
        parser.add_argument('-a', '--author', type=str, help='MetaMemo Author Name')
        parser.add_argument('-d', '--debug', action='store_true')
        parser.add_argument('-i', '--image', action='store_true')


    def handle(self, *args, **kwargs):
        self.channel = kwargs['channel']
        self.author = kwargs['author']
        self.debug = kwargs['debug']
        self.img_download = kwargs['image']
        self.source = 'Youtube'
        
        self.memo_author = MetaMemo.objects.get_or_create(name=self.author)
        self.memo_source = MemoSource.objects.get_or_create(name=self.source)
        
        self.memo_itens = MemoItem.objects.filter(author__name=self.author, source__name=self.source).values_list('original_id', flat=True)
        
        #Leva as configurações para o settings.py (que herdam do .env)
        self.apikey = getattr(settings, 'GOOGLE_YOUTUBE_CREDENTIALS', None)
        
        
        self.base_url = f'https://www.googleapis.com/youtube/v3/search?channelId={self.channel}&type=video&key={self.apikey}&maxResults=50&part=id'

        #url = f'https://www.googleapis.com/blogger/v3/blogs/'5199825393127499442/posts?key=AIzaSyAbHnIrSgZ9s-CqCKH_ERPJa8sW3IbDhok&maxResults=500&maxResults=500

        #url = f'https://api.crowdtangle.com/posts?token={apikey}&accounts={self.username}&sortBy=date&timeframe={interval}&count={pages}'
        self.parseUrl(self.base_url)

    def parseUrl(self, url):
        response = urllib.request.urlopen(url)
        if self.debug:
            print(f'Acessing {url}')
        
        posts_search = json.load(response)
        video_ids = []
        for video in posts_search['items']:
            video_ids.append(video['id']['videoId'])
        vids = ",".join(video_ids)

        api_url = f'https://www.googleapis.com/youtube/v3/videos?key={self.apikey}&part=snippet,statistics&id={vids}'

        if self.debug:
            print(f'Acessing {api_url}')
        
        response = urllib.request.urlopen(api_url)
        
        input_posts = json.load(response)

        if 'items' in input_posts:
            for i in input_posts['items']:
                post_id = i['id']
                if post_id in self.memo_itens:
                    if self.debug:
                        print(f"{post_id} already in base")
                        continue
                else:
                    if self.debug:
                        print(f"Saving {post_id}")
                    post = MemoItem()
                    post.author = self.memo_author[0]
                    post.source = self.memo_source[0]
                    
                post.content = i['snippet']['description']
                post.title = i['snippet']['title']
                post.extraction_date = datetime.datetime.now()
                post.content_date = i['snippet']['publishedAt']
                post.url = f'https://www.youtube.com/watch?v={i["id"]}'
                post.likes = i['statistics']['likeCount']
                post.shares = 0
                post.interactions = i['statistics']['commentCount']
                post.original_id = post_id
                post.raw = json.dumps(i, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                post.save()
        
        if 'nextPageToken' in posts_search:
            self.parseUrl(self.base_url+f'&pageToken={posts_search["nextPageToken"]}')
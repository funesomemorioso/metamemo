from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from django.utils import timezone
from metamemoapp.models import MetaMemo, MemoItem, MemoSource
import json, pprint, os, datetime
from telethon import TelegramClient
from decouple import config
from textwrap import shorten
from metamemoapp.tasks import download_img_async, download_async
from django.core.files.base import File
from asgiref.sync import sync_to_async
import io

TITLE_MAX_CHAR = 300

"""
Cada arquivo dentro de management/commands é um comando que pode ser rodado usando 'python manage.py nomedocomando'.
Handle() é a função executada pelo código.
A vantagem de fazer assim é que as libs e dependencias do Django já estão encapsuladas e você pode chamar essa função dentro do resto do código.
"""
    

class Command(BaseCommand):
    help = 'Importa de um usuário do telegram'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help='Telegram Username')
        parser.add_argument('-a', '--author', type=str, help='MetaMemo Author Name')
        parser.add_argument('-m', '--media', action='store_true')
        parser.add_argument('-l', '--limit', type=int, default=50, help='Post limits.')


    def handle(self, *args, **kwargs):
        self.username = kwargs['username']
        self.author = kwargs['author']
        self.video_download = kwargs['media']
        self.limit = kwargs['limit']

        self.memo_author = MetaMemo.objects.get_or_create(name=self.author)
        self.memo_source = MemoSource.objects.get_or_create(name='Telegram')
        
    
        self.memo_itens = list(MemoItem.objects.filter(author__name=self.author, source__name='Telegram').values_list('original_id', flat=True))
        
        

        self.telegram_api_id = config('TELEGRAM_API_ID', default='')
        self.telegram_api_hash = config('TELEGRAM_API_HASH', default='')
        
        if not self.telegram_api_hash and not self.telegram_api_id:
            print("You need to setup the API in .env")
            raise 
        
        self.client = TelegramClient('anon', self.telegram_api_id, self.telegram_api_hash)
        
        with self.client:
            self.client.loop.run_until_complete(self.getChat())

    async def getChat(self):
        chat = await self.client.get_input_entity(self.username)
        messages = await self.client.get_messages(chat, limit=self.limit)
        
        for i in messages:
            if f'{self.username}_{i.id}' in self.memo_itens:
                print("Done!")
                break
            else:
                post = MemoItem()
                post.author = self.memo_author[0]
                post.source = self.memo_source[0]
                post.title = shorten(i.text, TITLE_MAX_CHAR)
                post.content = i.text
                post.extraction_date = datetime.datetime.now()
                post.content_date = i.date
                post.url = ''
                post.likes = 0
                post.shares = i.forwards
                post.interactions = 0
                post.original_id = f'{self.username}_{i.id}'
                post.raw = i.to_json()
                print(post)
                await self.savePost(post)

                if i.video:
                    media = io.BytesIO()
                    await i.download_media(media)
                    await self.saveMedia(post, media, 'VIDEO')
                elif i.photo:
                    media = io.BytesIO()
                    await i.download_media(file=media)
                    await self.saveMedia(post, media, 'IMAGE')
    
    
    @sync_to_async  
    def savePost(self, post):
        post.save()

    @sync_to_async
    def saveMedia(self, post, media, mediatype):
        ext = {
            'IMAGE' : 'jpg',
            'VIDEO' : 'mp4'
        }

        post_id = post.original_id.split('_')[1]
        p = post.medias.create(original_url=f'https://t.me/{self.username}/{post_id}', original_id=post.original_id, status='DOWNLOADED', mediatype=mediatype, source=self.memo_source[0])
        p.media.save(f'{self.username}_{post_id}.{ext[mediatype]}', File(media))
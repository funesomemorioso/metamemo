import io
import time
from textwrap import shorten

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files.base import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from telethon import TelegramClient

from metamemoapp.models import MemoItem, MemoSource, MetaMemo

TITLE_MAX_CHAR = 300


class Command(BaseCommand):
    help = "Importa de um usuário do telegram"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Telegram Username")
        parser.add_argument("author", type=str, help="MetaMemo Author Name")
        parser.add_argument("-l", "--limit", type=int, default=300, help="Post limits.")

    def handle(self, *args, **kwargs):
        self.username = kwargs["username"]
        self.author = kwargs["author"]
        self.limit = kwargs["limit"]

        if not settings.TELEGRAM_API_ID or not settings.TELEGRAM_API_HASH:
            print("You need to setup the Telegram API credentials")
            raise

        self.memo_author = MetaMemo.objects.get_or_create(name=self.author)
        self.memo_source = MemoSource.objects.get_or_create(name="Telegram")
        self.memo_itens = set(
            MemoItem.objects.filter(author__name=self.author, source__name="Telegram").values_list(
                "original_id", flat=True
            )
        )
        self.client = TelegramClient(
            str(settings.TELEGRAM_SESSION_FILE.absolute()),
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH,
        )

        with self.client:
            self.client.loop.run_until_complete(self.getChat())

    async def getChat(self):
        chat = await self.client.get_input_entity(self.username)
        messages = await self.client.get_messages(chat, limit=self.limit)

        for message in messages:
            if f"{self.username}_{message.id}" in self.memo_itens:
                print(f"Done downloading messages for {self.username}.")
                break

            post = MemoItem()
            post.author = self.memo_author[0]
            post.source = self.memo_source[0]
            post.title = shorten(str(message.text or ""), TITLE_MAX_CHAR)
            post.content = message.text
            post.extraction_date = timezone.now()
            post.content_date = message.date
            post.url = ""
            post.likes = 0
            post.shares = message.forwards
            post.interactions = 0
            post.original_id = f"{self.username}_{message.id}"
            post.raw = message.to_json()
            print(post)
            await self.savePost(post)

            if message.photo or message.video:
                file_type = "IMAGE" if message.photo else "VIDEO"
                media = io.BytesIO()
                await message.download_media(media)
                await self.saveMedia(post, media, file_type)

    @sync_to_async
    def savePost(self, post):
        post.save()

    @sync_to_async
    def saveMedia(self, post, media, mediatype):
        ext = {"IMAGE": "jpg", "VIDEO": "mp4"}

        post_id = post.original_id.split("_")[1]
        p = post.medias.create(
            original_url=f"https://t.me/{self.username}/{post_id}",
            original_id=post.original_id,
            status="DOWNLOADED",
            mediatype=mediatype,
            source=self.memo_source[0],
        )
        p.media.save(f"{self.username}_{post_id}.{ext[mediatype]}", File(media))

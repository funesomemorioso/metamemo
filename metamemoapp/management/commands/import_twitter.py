import json
import time
from textwrap import shorten

import tweepy
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from metamemoapp.models import MemoItem, MemoSource, MetaMemo
from metamemoapp.tasks import download_async, download_img_async

TITLE_MAX_CHAR = 300

class Command(BaseCommand):
    help = "Importa de um usuário do twitter"

    def add_arguments(self, parser):
        parser.add_argument("-m", "--media", action="store_true")
        parser.add_argument("-r", "--refresh", action="store_true")
        parser.add_argument("-w", "--wait-time", type=int, default=60, help="Time to wait between each MetaMemo")

    def handle(self, *args, **kwargs):
        self.video_download = kwargs["media"]
        self.update = kwargs["refresh"]
        self.wait_time = kwargs["wait_time"]
        if not settings.TWITTER_BEARER_TOKEN:
            raise RuntimeError("You need to setup Twitter bearer token")

        self.memo_source, _ = MemoSource.objects.get_or_create(name="Twitter")
        for metamemo in MetaMemo.objects.all():
            if not metamemo.twitter_handle:
                continue
            print(f"Collecting Twitter for {metamemo.twitter_handle}")
            self.username = metamemo.twitter_handle
            self.memo_itens = MemoItem.objects.filter(author=metamemo, source=self.memo_source).values_list(
                "original_id", flat=True
            )
            self.client = tweepy.Client(settings.TWITTER_BEARER_TOKEN)
            self.user = self.client.get_user(username=self.username)
            self.getTweets()
            time.sleep(self.wait_time)

    def getTweets(self, paginationToken=None):
        finished = False
        input_posts = self.client.get_users_tweets(
            self.user.data.id,
            media_fields=["url", "type", "media_key"],
            expansions="attachments.media_keys",
            tweet_fields="created_at,public_metrics",
            max_results=100,
            pagination_token=paginationToken,
        )

        # Aqui estou usando o MemoItem() para instancear um objeto que defini
        # lá no models.  E a função save() para salvar efetivamente no banco.
        # Tem um outro jeito de fazer onde você comita todas as alterações e
        # salva de uma vez, acho que vale refatorar depois.
        tweet_media = {}

        if "media" in input_posts.includes:
            for m in input_posts.includes["media"]:
                if m["type"] == "video":
                    tweet_media[m["media_key"]] = {"mediatype": "VIDEO", "url": m["url"]}
                elif m["type"] == "photo":
                    tweet_media[m["media_key"]] = {"mediatype": "IMAGE", "url": m["url"]}

        for i in input_posts.data:
            if str(i.id) in self.memo_itens:
                if not self.update:
                    finished = True
                    break
            else:
                post = MemoItem()
                post.author = self.memo_author
                post.source = self.memo_source
                post.title = shorten(i.text, TITLE_MAX_CHAR)
                post.content = i.text
                post.extraction_date = timezone.now()
                post.content_date = i.created_at
                post.url = f"https://twitter.com/{self.user.data.username}/status/{i.id}"
                post.likes = i.public_metrics["like_count"]
                post.shares = i.public_metrics["retweet_count"]
                post.interactions = i.public_metrics["reply_count"]
                post.original_id = i.id
                post.raw = json.dumps(dict(i), sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                post.save()

                if i.attachments:
                    for m in i.attachments["media_keys"]:
                        if m not in tweet_media:
                            continue
                        media = tweet_media[m]
                        if media["mediatype"] == "VIDEO":
                            p = post.medias.create(
                                original_url=f"https://twitter.com/{self.user.data.username}/status/{i.id}",
                                original_id=m,
                                status="INITIAL",
                                mediatype="VIDEO",
                                source=self.memo_source,
                            )
                            if self.video_download:
                                p.status = "DOWNLOADING"
                                p.save()
                                post.save()
                                download_async.apply_async(
                                    kwargs={"url": p.original_url, "mediatype": "VIDEO"}, queue="twitter"
                                )
                        elif media["mediatype"] == "IMAGE":
                            p = post.medias.create(
                                original_url=media["url"], original_id=m, status="INITIAL", mediatype="IMAGE"
                            )
                            p.save()
                            post.save()
                            download_img_async.apply_async(kwargs={"url": media["url"], "pk": p.pk}, queue="twitter")

        if "next_token" in input_posts.meta and not finished:
            self.getTweets(paginationToken=input_posts.meta["next_token"])

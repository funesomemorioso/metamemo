import datetime
import json
import urllib
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from metamemoapp.models import MemoItem, MemoSource, MetaMemo
from metamemoapp.tasks import download_async

TITLE_MAX_CHAR = 300


class Command(BaseCommand):
    help = "Importa de um canal no Youtube"

    def add_arguments(self, parser):
        parser.add_argument("-d", "--debug", action="store_true")
        parser.add_argument("-m", "--media", action="store_true")
        parser.add_argument("-t", "--time", type=int, default=0, help="Time in days")
        parser.add_argument("-w", "--wait-time", type=int, default=60, help="Time to wait between each MetaMemo")

    def handle(self, *args, **kwargs):
        self.debug = kwargs["debug"]
        self.video_download = kwargs["media"]
        self.days = kwargs["time"]
        self.wait_time = kwargs["wait_time"]
        if not settings.GOOGLE_YOUTUBE_CREDENTIALS:
            raise RuntimeError("You need to setup the YouTube API credentials")

        self.memo_source, _ = MemoSource.objects.get_or_create(name="Youtube")
        for metamemo in MetaMemo.objects.all():
            if not metamemo.youtube_handle:
                continue
            print(f"Collecting YouTube for {metamemo.youtube_handle}")
            self.channel = metamemo.youtube_handle
            self.memo_author = metamemo
            self.memo_itens = MemoItem.objects.filter(author=metamemo, source=self.memo_source).values_list(
                "original_id", flat=True
            )
            # Leva as configurações para o settings.py (que herdam do .env)
            self.apikey = settings.GOOGLE_YOUTUBE_CREDENTIALS
            self.base_url = f"https://www.googleapis.com/youtube/v3/search?channelId={self.channel}&type=video&key={self.apikey}&maxResults=50&part=id"
            if self.days:
                timeAgo = (timezone.now() - datetime.timedelta(self.days)).strftime("%Y-%m-%dT00:00:00Z")
                self.base_url += f"&publishedAfter={timeAgo}"
            self.parseUrl(self.base_url)
            time.sleep(self.wait_time)

    def parseUrl(self, url):
        if self.debug:
            print(f"Acessing {url}")
        response = urllib.request.urlopen(url)
        posts_search = json.load(response)
        video_ids = []
        for video in posts_search["items"]:
            if video["id"]["videoId"] not in self.memo_itens:
                video_ids.append(video["id"]["videoId"])
        if video_ids:
            vids = ",".join(video_ids)
            api_url = (
                f"https://www.googleapis.com/youtube/v3/videos?key={self.apikey}&part=snippet,statistics&id={vids}"
            )
            if self.debug:
                print(f"Acessing {api_url}")

            response = urllib.request.urlopen(api_url)
            input_posts = json.load(response)
            if "items" in input_posts:
                for i in input_posts["items"]:
                    post_id = i["id"]
                    if post_id in self.memo_itens:
                        if self.debug:
                            print(f"{post_id} already in base")
                    else:
                        if self.debug:
                            print(f"Saving {post_id}")
                        post = MemoItem()
                        post.author = self.memo_author
                        post.source = self.memo_source
                        post.content = i["snippet"]["description"]
                        post.title = i["snippet"]["title"]
                        post.extraction_date = timezone.now()
                        post.content_date = i["snippet"]["publishedAt"]
                        post.url = f'https://www.youtube.com/watch?v={i["id"]}'
                        post.likes = i["statistics"]["likeCount"]
                        post.shares = 0
                        post.interactions = i["statistics"]["commentCount"]
                        post.original_id = post_id
                        post.raw = json.dumps(i, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                        post.save()
                        p = post.medias.create(
                            original_url=post.url,
                            original_id=post_id,
                            status="INITIAL",
                            mediatype="VIDEO",
                            source=self.memo_source,
                        )

                    if p and self.video_download:
                        p.status = "DOWNLOADING"
                        p.save()
                        post.save()
                        download_async.apply_async(
                            kwargs={"url": p.original_url, "mediatype": "VIDEO"}, queue="youtube"
                        )

        if "nextPageToken" in posts_search:
            self.parseUrl(self.base_url + f'&pageToken={posts_search["nextPageToken"]}')

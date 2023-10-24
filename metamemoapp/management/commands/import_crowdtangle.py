import datetime
import json
import urllib
import time
from textwrap import shorten

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from metamemoapp.models import MemoItem, MemoSource, MetaMemo
from metamemoapp.tasks import download_async, download_img_async

TITLE_MAX_CHAR = 300


class Command(BaseCommand):
    help = "Importa de um arquivo de facebook/instagram via Crowdtangle"

    def add_arguments(self, parser):
        parser.add_argument("-c", "--clear", action="store_true")
        parser.add_argument("-s", "--source", type=str, help="Source", choices=["Facebook", "Instagram"])
        parser.add_argument("-d", "--debug", action="store_true")
        parser.add_argument("-i", "--image", action="store_true")
        parser.add_argument("-m", "--media", action="store_true")
        parser.add_argument("-w", "--wait-time", type=int, default=60, help="Time to wait between each MetaMemo")

    def handle(self, *args, **kwargs):
        self.clear = kwargs["clear"]
        self.source = kwargs["source"]
        self.debug = kwargs["debug"]
        self.image_download = kwargs["image"]
        self.video_download = kwargs["media"]
        self.wait_time = kwargs["wait_time"]
        apikey = None
        if self.source == "Facebook":
            apikey = settings.CROWDTANGLE_FACEBOOK_API_KEY
        elif self.source == "Instagram":
            apikey = settings.CROWDTANGLE_INSTAGRAM_API_KEY
        if not apikey:
            raise RuntimeError(f"You need to setup the Crowdtangle API credentials for {self.source}")

        handle_field = {"Facebook": "facebook_handle", "Instagram": "instagram_handle"}[self.source]
        self.memo_source, _ = MemoSource.objects.get_or_create(name=self.source)
        for metamemo in MetaMemo.objects.all():
            self.username = getattr(metamemo, handle_field, None)
            if not self.username:
                continue
            print(f"Collecting {self.source} for {self.username}")
            self.memo_author = metamemo
            if self.clear:
                # Esvazia lista de ids caso passe a flag --clear
                # TODO: excluir os posts (não foi feito para manter os posts p/ debug)
                self.memo_itens = []
            else:
                self.memo_itens = MemoItem.objects.filter(author=metamemo, source=self.memo_source).values_list(
                    "original_id", flat=True
                )

            pages = settings.CROWDTANGLE_POSTS_COUNT
            interval = urllib.parse.quote_plus(settings.CROWDTANGLE_POSTS_INTERVAL)
            # TODO: should get more pages?
            url = f"https://api.crowdtangle.com/posts?token={apikey}&accounts={self.username}&sortBy=date&timeframe={interval}&count={pages}"
            self.parseUrl(url)
            time.sleep(self.wait_time)

    def parseUrl(self, url):
        if self.debug:
            print(f"Acessing {url}")
        response = urllib.request.urlopen(url)
        input_posts = json.load(response)

        if input_posts["status"] == 200:
            for i in input_posts["result"]["posts"]:
                post_id = i["id"].split("|")[1]
                if post_id in self.memo_itens:
                    if self.clear:
                        break
                    else:
                        if self.debug:
                            print(f"{post_id} already in base")
                else:
                    i["date"] = datetime.datetime.strptime(i["date"] + "Z", "%Y-%m-%d %H:%M:%S%z")
                    if self.debug:
                        print(f"Saving {post_id}")
                    post = MemoItem()
                    post.author = self.memo_author
                    post.source = self.memo_source

                    if i["platform"] == "Facebook":
                        if "message" in i:
                            post.content = i["message"]
                            post.title = shorten(i["message"].replace("\n", " "), TITLE_MAX_CHAR)
                        else:
                            post.title = ""  # FIX
                            post.content = ""
                        post.extraction_date = timezone.now()
                        post.content_date = i["date"]
                        post.url = i["postUrl"]
                        post.likes = i["statistics"]["actual"]["likeCount"]
                        post.shares = i["statistics"]["actual"]["shareCount"]
                        post.interactions = i["statistics"]["actual"]["commentCount"]
                    elif i["platform"] == "Instagram":
                        if "description" in i:
                            post.title = shorten(i["description"].replace("\n", " "), TITLE_MAX_CHAR)
                            post.content = i["description"]
                        elif "imageText" in i:
                            post.title = shorten(i["imageText"].replace("\n", " "), TITLE_MAX_CHAR)
                            post.content = i["imageText"]
                        else:
                            post.title = ""
                            post.content = ""

                        post.extraction_date = timezone.now()
                        post.content_date = i["date"]
                        post.url = i["postUrl"]
                        post.likes = i["statistics"]["actual"]["favoriteCount"]
                        post.interactions = i["statistics"]["actual"]["commentCount"]

                    post.original_id = post_id
                    post.raw = json.dumps(i, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                    post.save()

                    # Cria um metaitem com status INITIAL caso existam vídeos
                    p = None
                    if i["platform"] == "Facebook" and i["type"] in ["live_video_complete", "native_video"]:
                        if "link" in i:
                            p = post.medias.create(
                                original_url=i["link"],
                                original_id=post_id,
                                status="INITIAL",
                                mediatype="VIDEO",
                                source=self.memo_source,
                            )
                        else:
                            p = post.medias.create(
                                original_url=i["postUrl"],
                                original_id=post_id,
                                status="INITIAL",
                                mediatype="VIDEO",
                                source=self.memo_source,
                            )
                    elif i["platform"] == "Instagram" and i["type"] == "video":
                        p = post.medias.create(
                            original_url=i["postUrl"],
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
                            kwargs={"url": p.original_url, "mediatype": "VIDEO"}, queue=i["platform"].lower()
                        )

                    if "media" in i:
                        for m in i["media"]:
                            if m["type"] == "photo":
                                p = post.medias.create(
                                    original_url=i["postUrl"], original_id=post_id, status="INITIAL", mediatype="IMAGE"
                                )
                                if self.image_download:
                                    download_img_async.apply_async(
                                        kwargs={"url": m["url"], "pk": p.pk}, queue=i["platform"].lower()
                                    )

        if "nextPage" in input_posts["result"]["pagination"]:
            self.parseUrl(input_posts["result"]["pagination"]["nextPage"])

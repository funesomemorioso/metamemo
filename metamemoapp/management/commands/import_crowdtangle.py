import json
import urllib
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
        parser.add_argument("-u", "--username", type=str, help="Account Username")
        parser.add_argument("-a", "--author", type=str, help="MetaMemo Author Name")
        parser.add_argument("-c", "--clear", action="store_true")
        parser.add_argument("-s", "--source", type=str, help="Source")
        parser.add_argument("-d", "--debug", action="store_true")
        parser.add_argument("-i", "--image", action="store_true")
        parser.add_argument("-m", "--media", action="store_true")

    def handle(self, *args, **kwargs):
        self.username = kwargs["username"]
        self.author = kwargs["author"]
        self.clear = kwargs["clear"]
        self.source = kwargs["source"]
        self.debug = kwargs["debug"]
        self.image_download = kwargs["image"]
        self.video_download = kwargs["media"]

        self.memo_author = MetaMemo.objects.get_or_create(name=self.author)
        self.memo_source = MemoSource.objects.get_or_create(name=self.source)

        self.memo_itens = MemoItem.objects.filter(author__name=self.author, source__name=self.source).values_list(
            "original_id", flat=True
        )

        # Esvazia lista de ids caso passe a flag --clear;
        # TODO: Excluir os posts em caso de clear. Não fiz ainda para manter os posts p/ debug.
        if self.clear:
            self.memo_itens = []

        # Leva as configurações para o settings.py (que herdam do .env)
        if self.source == "Facebook":
            apikey = getattr(settings, "CROWDTANGLE_FACEBOOK_API_KEY", None)
        elif self.source == "Instagram":
            apikey = getattr(settings, "CROWDTANGLE_INSTAGRAM_API_KEY", None)
        pages = getattr(settings, "CROWDTANGLE_POSTS_COUNT", 100)
        interval = urllib.parse.quote_plus(getattr(settings, "CROWDTANGLE_POSTS_INTERVAL", "5 DAY"))

        url = f"https://api.crowdtangle.com/posts?token={apikey}&accounts={self.username}&sortBy=date&timeframe={interval}&count={pages}"
        self.parseUrl(url)

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
                        print("Done!")
                        break
                    else:
                        if self.debug:
                            print(f"{post_id} already in base")
                else:
                    if self.debug:
                        print(f"Saving {post_id}")
                    post = MemoItem()
                    post.author = self.memo_author[0]
                    post.source = self.memo_source[0]

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
                                source=self.memo_source[0],
                            )
                        else:
                            p = post.medias.create(
                                original_url=i["postUrl"],
                                original_id=post_id,
                                status="INITIAL",
                                mediatype="VIDEO",
                                source=self.memo_source[0],
                            )
                    elif i["platform"] == "Instagram" and i["type"] == "video":
                        p = post.medias.create(
                            original_url=i["postUrl"],
                            original_id=post_id,
                            status="INITIAL",
                            mediatype="VIDEO",
                            source=self.memo_source[0],
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

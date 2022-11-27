import csv
import json
from textwrap import shorten

from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from metamemoapp.models import MemoItem, MemoSource, MetaMemo

TITLE_MAX_CHAR = 300


class Command(BaseCommand):
    help = "Importa de um arquivo de facebook/instagram via CSV do Crowdtangle"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--filename", type=str, help="CSV Filename")
        parser.add_argument("-d", "--debug", action="store_true")
        parser.add_argument("-i", "--image", action="store_true")

    def handle(self, *args, **kwargs):
        self.debug = kwargs["debug"]
        self.img_download = kwargs["image"]
        self.filename = kwargs["filename"]

        self.memo_itens = MemoItem.objects.all().values_list("original_id", flat=True)
        # Leva as configurações para o settings.py (que herdam do .env)

        datafile = open(self.filename, "r", encoding="utf-8-sig")
        print("Loading file...")
        posts = csv.DictReader(datafile)
        posts.fieldnames = [x.lower().replace(" ", "_") for x in posts.fieldnames]

        post_objects = []
        for p in posts:
            if "facebook_d" in p:
                post_id = p["url"].split("/")[-1]
            elif "photo" in p:
                post_id = p["url"][:-1].split("/")[-1]  # hackish para pegar id do post
            if post_id in self.memo_itens:
                if self.debug:
                    print("Post already in database")
                continue
            post = MemoItem()
            post.original_id = post_id
            if "facebook_id" in p:
                post.source = MemoSource.objects.get_or_create(name="Facebook")[0]
                post.author = MetaMemo.objects.get_or_create(
                    facebook_handle=p["user_name"], defaults={"name": p["page_name"]}
                )[0]
                post.content = p["message"]
                post.title = shorten(p["message"].replace("\n", " "), TITLE_MAX_CHAR)
                post.extraction_date = timezone.now()
                post.content_date = p["post_created"].replace("EST", "").replace("EDT", "").strip()
                post.url = p["url"]
                post.likes = int(p["likes"])
                post.shares = int(p["shares"])
                post.interactions = int(p["comments"])
                post.raw = json.dumps(p, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                post_objects.append(post)
            elif "photo" in p and p["url"]:
                post.source = MemoSource.objects.get_or_create(name="Instagram")[0]
                post.author = MetaMemo.objects.get_or_create(
                    instagram_handle=p["user_name"], defaults={"name": p["account"]}
                )[0]
                post.content = p["description"]
                post.title = shorten(p["description"].replace("\n", " "), TITLE_MAX_CHAR)
                post.extraction_date = timezone.now()
                post.content_date = p["post_created"].replace("EST", "").replace("EDT", "").strip()
                post.url = p["url"]
                post.likes = int(p["likes"])
                post.interactions = int(p["comments"])
                post.raw = json.dumps(p, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                post_objects.append(post)

        print(f"Creating {len(post_objects)} records...")
        posts_created = MemoItem.objects.bulk_create(post_objects, batch_size=100)
        print("Creating media records...")
        for poid in posts_created:
            post = MemoItem.objects.get(original_id=poid.original_id)
            p = json.loads(post.raw)
            if p["type"] in ["Native Video", "Live Video Complete", "YouTube", "Live Video Scheduled", "Video"]:
                if "link" in p:
                    post.medias.get_or_create(
                        original_url=p["link"],
                        original_id=post.original_id,
                        mediatype="VIDEO",
                        defaults={"status": "INITIAL"},
                    )
                else:
                    post.medias.get_or_create(
                        original_url=p["postUrl"],
                        original_id=post.original_id,
                        mediatype="VIDEO",
                        defaults={"status": "INITIAL"},
                    )
            elif "photo" in p:
                post.medias.get_or_create(
                    original_url=p["photo"],
                    original_id=post.original_id,
                    mediatype="IMAGE",
                    defaults={"status": "INITIAL"},
                )
            elif p["type"] == "Photo":
                post.medias.get_or_create(
                    original_url=p["link"],
                    original_id=post.original_id,
                    mediatype="IMAGE",
                    defaults={"status": "INITIAL"},
                )

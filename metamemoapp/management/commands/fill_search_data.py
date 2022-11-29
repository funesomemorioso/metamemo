from django.core.management.base import BaseCommand
from django.db import models, transaction

from tqdm import tqdm

from metamemoapp.models import MemoContext, MemoItem, MemoMedia, NewsItem


class Command(BaseCommand):
    help = "Save objects with text to trigger search_data filling"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            objs = MemoItem.objects.filter(
                models.Q(search_data__isnull=True)
                & (
                    models.Q(title__isnull=False) | models.Q(content__isnull=False)
                )
            )
            for obj in tqdm(objs, total=objs.count(), desc="MemoItem"):
                obj.save()

        with transaction.atomic():
            objs = MemoMedia.objects.filter(
                models.Q(search_data__isnull=True)
                & models.Q(transcription__isnull=False)
            )
            for obj in tqdm(objs, total=objs.count(), desc="MemoMedia"):
                obj.save()

        with transaction.atomic():
            objs = MemoContext.objects.filter(
                models.Q(search_data__isnull=True)
                & models.Q(context__isnull=False)
            )
            for obj in tqdm(objs, total=objs.count(), desc="MemoContext"):
                obj.save()

        with transaction.atomic():
            objs = NewsItem.objects.filter(
                models.Q(search_data__isnull=True)
                & (
                    models.Q(title__isnull=False) | models.Q(text__isnull=False)
                )
            )
            for obj in tqdm(objs, total=objs.count(), desc="NewsItem"):
                obj.save()

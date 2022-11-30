import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from metamemoapp.models import MemoItem


class Command(BaseCommand):
    help = "Export database executing SQL directly"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        filename = Path(settings.BASE_DIR) / "dump" / f"{today}-database.csv"
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        print(f"Exporting to {filename}")
        with open(filename, mode="w") as fobj:
            writer = csv.writer(fobj)
            for row in MemoItem.objects.export_csv():
                writer.writerow(row)

from django.core.management.base import BaseCommand

from metamemoapp.models import MemoMedia
from metamemoapp.tasks import download_img_async, download_async
from metamemo.celery import app

class Command(BaseCommand):
    help = 'Download media from a few random medias'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int, help='How many to download?')
        parser.add_argument('-t', '--type', type=str, help='Which types?')
        parser.add_argument('-f', '--fake', action='store_true')
        parser.add_argument('-r', '--retry', action='store_true')
        parser.add_argument('-q', '--queue', type=str, help='Queue to check')
    def handle(self, *args, **kwargs):
        self.count = kwargs['number']
        self.type = kwargs['type']
        self.fake = kwargs['fake']
        self.retry = kwargs['retry']
        self.queue = kwargs['queue']

        if self.queue:
            q = len(app.inspect().reserved()[self.queue]
            if q==0:
                return None

        self.medias = MemoMedia.objects.filter(media='').exclude(status='DOWNLOADING')
        if not self.retry:
            self.medias = self.medias.exclude(status='FAILED_DOWNLOAD')
        if self.type:
            self.medias = self.medias.filter(mediatype=self.type)
        
        for p in self.medias[0:self.count]:
            print(f'Downloading {p.pk} {p.mediatype} from {p.original_url}')
            print(p.media)
            if p.mediatype == 'VIDEO' and not self.fake:
                p.status = 'DOWNLOADING'
                p.save()
                download_async.apply_async(kwargs={'url': p.original_url, 'mediatype': 'VIDEO'}, queue="fastlane")
            elif p.mediatype=='IMAGE' and not self.fake:
                download_img_async.apply_async(kwargs={'url' : p.original_url, 'pk' : p.pk}, queue="fastlane")
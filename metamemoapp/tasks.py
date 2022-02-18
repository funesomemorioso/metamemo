from celery import shared_task
from metamemoapp.utils import google_transcribe
from metamemoapp.models import MemoMedia

from django.core.files.base import File
import tempfile, mimetypes
import youtube_dl

@shared_task
def transcribe_async(pk):
    print(pk)
    i = MemoMedia.objects.get(pk=pk)
    i.transcription = google_transcribe(i.media.path)
    i.status = 'TRANSCRIBED'
    i.save()

@shared_task
def download_async(pk):
    i = MemoMedia.objects.get(pk=pk)

    with tempfile.TemporaryDirectory() as tempdirname:
        
        ydl_opts = {
            'outtmpl': f'{tempdirname}/{i.original_id}.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks':[]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([i.original_url])
    
        with open(f'{tempdirname}/{i.original_id}.mp4', 'rb') as tmpfile:
            media_file = File(tmpfile)
            result = i.media.save(f"{i.original_id}.mp4", media_file)
            i.status = 'DOWNLOADED'
            #self.mimetype = mimetype
            i.save()
    return True
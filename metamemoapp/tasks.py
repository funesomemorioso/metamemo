from celery import shared_task
from metamemoapp.utils import google_transcribe
from metamemoapp.models import MemoMedia

@shared_task
def transcribe_async(pk):
    print(pk)
    i = MemoMedia.objects.get(pk=pk)
    i.transcription = google_transcribe(i.media.path)
    i.status = 'TRANSCRIBED'
    i.save()
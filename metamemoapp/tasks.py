from django.conf import settings

from celery import shared_task, chain
from celery_progress.backend import ProgressRecorder
from metamemoapp.utils import google_transcribe
from metamemoapp.models import MemoMedia

from django.core.files.base import File
import tempfile, mimetypes
import youtube_dl, urllib, os

from pydub import AudioSegment
import io, os, wave, time

from google.cloud import storage
from google.cloud import speech


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= getattr(settings, "GOOGLE_APPLICATION_CREDENTIALS", None)
METAMEMO_DEFAULT_LANGUAGE = getattr(settings, "METAMEMO_DEFAULT_LANGUAGE", "pt-BR")

@shared_task
def convert_to_wave_async(media):
    sound = AudioSegment.from_file(media.file)
    buf = io.BytesIO()

    if sound.channels > 1:
        sound = sound.set_channels(1)
    sound.export(buf, format="wav")
    return buf, sound.frame_rate

@shared_task
def upload_to_google_async(url):
    media = MemoMedia.objects.filter(original_url=url, mediatype='VIDEO').first().media
    buf, frame_rate = convert_to_wave_async(media)
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('metamemo')
    blob = bucket.blob(media.file.name)

    blob.upload_from_file(buf)
    return {'gcs_uri' : 'gs://metamemo/' + media.file.name, 'frame_rate' : frame_rate}

@shared_task
def get_transcription_async(operation):
    transcript = ''
    response = operation.result(timeout=10000)
    for r in response.results:
        transcript += r.alternatives[0].transcript

    #delete blob
    return transcript


@shared_task
def transcribe_on_google_async(info):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=info['gcs_uri'])

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=info['frame_rate'],
        language_code=METAMEMO_DEFAULT_LANGUAGE)

    # Detects speech in the audio file
    operation = client.long_running_recognize(request={"config":config, "audio":audio})
    transcript = get_transcription_async(operation)
    return transcript
    
@shared_task
def transcribe_async(url, mediatype):
    i = MemoMedia.objects.filter(original_url=url, mediatype=mediatype).first()
    try:
        i.transcription = (upload_to_google_async.s() | transcribe_on_google_async.s()).delay(i.original_url)
        i.status = 'TRANSCRIBED'
        i.save()
    except:
        i.status = 'FAILED_TRANSCRIBE'
        i.save()
        raise Exception()


@shared_task(bind=True)
def download_async(self, url, mediatype):
    progress_recorder = ProgressRecorder(self)
    
    if mediatype=='VIDEO':
        i = MemoMedia.objects.filter(original_url=url, mediatype=mediatype).first()
    
        def progress_hook(info):
            state, meta = progress_recorder.set_progress(info['downloaded_bytes'],info['total_bytes'])
            i.progress=meta['percent']
            i.save()

        item = i.memoitem_set.first()
        try:
            with tempfile.TemporaryDirectory() as tempdirname:
                
                ydl_opts = {
                    'outtmpl': f'{tempdirname}/{i.original_id}.%(ext)s',
                    'merge_output_format': 'mp4',
                    'progress_hooks':[progress_hook]
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([i.original_url])
            
                with open(f'{tempdirname}/{i.original_id}.mp4', 'rb') as tmpfile:
                    media_file = File(tmpfile)
                    result = i.media.save(f"{item.source.name.lower()}_{i.original_id}.mp4", media_file)
                    i.status = 'DOWNLOADED'
                    i.save()
        except:
            i.status = 'FAILED_DOWNLOAD'
            i.save()
            raise Exception()



@shared_task
def download_img_async(pk, url):
    result = urllib.request.urlopen(url)
    i = MemoMedia.objects.get(pk=pk)
    try:
        filename = os.path.basename(url)
        i.media.save(f'{i.original_id}_{filename}', File(result))
        i.status = 'DOWNLOADED'
        i.save()
    except:
        i.status = 'FAILED_DONWLOAD'
        i.save()

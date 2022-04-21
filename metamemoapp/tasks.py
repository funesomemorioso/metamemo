from django.conf import settings

from celery import shared_task, chain
from celery_progress.backend import ProgressRecorder
from metamemoapp.utils import google_transcribe
from metamemoapp.models import MemoMedia

from django.core.files.base import File
import tempfile, mimetypes
import urllib, os


from pydub import AudioSegment
import io, os, wave, time

from google.cloud import storage
from google.cloud import speech
from yt_dlp import YoutubeDL
from youtube_dl import YoutubeDL as OriginalYoutubeDL


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= getattr(settings, "GOOGLE_APPLICATION_CREDENTIALS", None)
METAMEMO_DEFAULT_LANGUAGE = getattr(settings, "METAMEMO_DEFAULT_LANGUAGE", "pt-BR")

@shared_task
def convert_to_wave_async(media):
    sound = AudioSegment.from_file(media.file)
    buf = io.BytesIO()

    if sound.channels > 1:
        sound = sound.set_channels(1)
    
    sound = sound.set_sample_width(2)
    sound.export(buf, format="wav")
    return buf, sound.frame_rate

@shared_task
def upload_to_google_async(result):
    media = MemoMedia.objects.filter(original_url=result['original_url'], mediatype='VIDEO').first().media
    buf, frame_rate = convert_to_wave_async(media)
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('metamemo')
    blob = bucket.blob(media.file.name)

    blob.upload_from_file(buf)
    result['gcs_uri'] = 'gs://metamemo/' + media.file.name
    result['frame_rate'] = frame_rate
    return result

@shared_task
def transcribe_on_google_async(result):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=result['gcs_uri'])

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=result['frame_rate'],
        language_code=METAMEMO_DEFAULT_LANGUAGE)

    # Detects speech in the audio file
    operation = client.long_running_recognize(request={"config":config, "audio":audio})
    result['transcript'] = ''
    response = operation.result(timeout=10000)
    for r in response.results:
        result['transcript'] += r.alternatives[0].transcript

    return result

@shared_task
def save_transcription_async(result):
    videos = MemoMedia.objects.filter(original_url=result['original_url'], mediatype='VIDEO')
    for i in videos:
        i.transcription = result['transcript']
        i.status = 'TRANSCRIBED'
        i.save(update_fields=['status','transcription'])

@shared_task
def transcribe_async(url, mediatype):
    i = MemoMedia.objects.filter(original_url=url, mediatype=mediatype).first()
    try:
        t = (upload_to_google_async.s() | transcribe_on_google_async.s() | save_transcription_async.s()).delay({'original_url' : url})
        i.status = 'TRANSCRIBING'
        i.save(update_fields=['status',])
    except:
        i.status = 'FAILED_TRANSCRIBE'
        i.save(update_fields=['status',])
        raise Exception()


@shared_task(bind=True)
def download_async(self, url, mediatype):
    self.url = url
    self.videos = MemoMedia.objects.filter(original_url=url, mediatype='VIDEO')
    self.first =  self.videos.first()
    self.progress_recorder = ProgressRecorder(self)

    def progress_hook(info):
        if 'downloaded_bytes' in info:
            state, meta = self.progress_recorder.set_progress(info['downloaded_bytes'],info['total_bytes'])
            self.first.progress=meta['percent']
            self.first.save()
    
    def get_filename(tempdirname):
        for ext in ['mp4', 'webm', 'mkv']:
            filename = f'{tempdirname}/{self.first.original_id}.{ext}'
            if os.path.isfile(filename):
                return filename, ext

    with tempfile.TemporaryDirectory() as tempdirname:

        ydl_opts = {
            'outtmpl': f'{tempdirname}/{self.first.original_id}.%(ext)s',
            'progress_hooks':[progress_hook],
            'format':'bestvideo+bestaudio/webm/mp4',
        }

        try:
            YoutubeDL(ydl_opts).download([self.url])
        except:
            try:
                OriginalYoutubeDL(ydl_opts).download([self.url])
            except:
                self.first.status = 'FAILED_DOWNLOAD'
                self.first.save(update_fields=['status',])
                raise Exception()

        filename, ext = get_filename(tempdirname)

        with open(filename, 'rb') as tmpfile:
            self.first.media.save(f'{self.first.original_id}.{ext}', File(tmpfile))
            self.first.status = 'DOWNLOADED'
            self.first.save()
            for v in self.videos[1:]: #adiciona media nos outros memomedia
                v.media = self.first.media
                v.status = 'DOWNLOADED'
                v.save(update_fields=['status', 'media'])

        return self.first.media.url


@shared_task
def download_img_async(pk, url):
    result = urllib.request.urlopen(url)
    i = MemoMedia.objects.get(pk=pk)
    try:
        filename = os.path.basename(url)
        i.media.save(f'{i.original_id}_{filename}', File(result))
        i.status = 'DOWNLOADED'
        i.save(update_fields=['status', 'media'])
    except:
        i.status = 'FAILED_DONWLOAD'
        i.save(update_fields=['status',])

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
        i.save()

@shared_task
def transcribe_async(url, mediatype):
    i = MemoMedia.objects.filter(original_url=url, mediatype=mediatype).first()
    try:
        t = (upload_to_google_async.s() | transcribe_on_google_async.s() | save_transcription_async.s()).delay({'original_url' : url})
        i.status = 'TRANSCRIBING'
        i.save()
    except:
        i.status = 'FAILED_TRANSCRIBE'
        i.save()
        raise Exception()


@shared_task(bind=True)
def download_async(self, url, mediatype):
    progress_recorder = ProgressRecorder(self)
    
    if mediatype=='VIDEO':
        videos = MemoMedia.objects.filter(original_url=url, mediatype=mediatype)
    
        i = videos.first()
        
        memoitem = i.memoitem_set.first()
        if memoitem:
            source = memoitem.source.name.upper()
        elif i.source:
            source = i.source
        else:
            source = 'NOCOOKIE'
            
        def progress_hook(info):
            if 'downloaded_bytes' in info:
                state, meta = progress_recorder.set_progress(info['downloaded_bytes'],info['total_bytes'])
                i.progress=meta['percent']
                i.save()

        try:
            with tempfile.TemporaryDirectory() as tempdirname:

                ydl_opts = {
                    'outtmpl': f'{tempdirname}/{i.original_id}.%(ext)s',
                    'progress_hooks':[progress_hook],
                    'format':'bestvideo+bestaudio/webm/mp4',
                    'cookiefile':getattr(settings, f'{source.upper()}_COOKIES', None)
                }

                try:
                    info = YoutubeDL(ydl_opts).extract_info(i.original_url, download=False)
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([i.original_url])
                except:#try with other download method
                    info = OriginalYoutubeDL(ydl_opts).extract_info(i.original_url, download=False)
                    with OriginalYoutubeDL(ydl_opts) as oydl:
                        oydl.download([i.original_url])

                if 'ext' in info:
                    ext = info['ext']
                elif '_type' in info and info['_type'] == 'playlist':
                    ext = info['entries'][0]['ext']
     
                filename = f'{tempdirname}/{i.original_id}.{ext}'
                if not os.path.isfile(filename):
                    filename = f'{tempdirname}/{i.original_id}.mkv' #hackish para mkv
                
                with open(filename, 'rb') as tmpfile:
                    media_file = File(tmpfile)
                    media = i.media.save(f'{source.lower()}_{i.original_id}.{ext}', media_file)
                    i.status = 'DOWNLOADED'
                    i.save()
                    for v in videos[1:]: #adiciona media nos outros memomedia
                        v.media = i.media
                        v.status = 'DOWNLOADED'
                        v.save()

            
            return i.media.url
            
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

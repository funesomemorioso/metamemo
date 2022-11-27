import datetime
import io
import re

import yake
from django.conf import settings
from django.utils import timezone
from google.cloud import speech, storage
from pydub import AudioSegment


def parse_date(content_date):
    mes = {
        "jan": 1,
        "fev": 2,
        "mar": 3,
        "abr": 4,
        "mai": 5,
        "jun": 6,
        "jul": 7,
        "ago": 8,
        "set": 9,
        "out": 10,
        "nov": 11,
        "dez": 12,
    }
    c = re.search("([0-9]{1,2})\.([a-z]{3})\.([0-9]{1,4}) à[s]? ([0-9]{1,2})h([0-9]{1,2})", content_date)
    return datetime.datetime(
        int(c[3]),
        mes[c[2]],
        int(c[1]),
        int(c[4]),
        int(c[5]),
        0,
        tzinfo=timezone.get_default_timezone(),
    )


def convert_to_wav(audio_file):
    sound = AudioSegment.from_file(audio_file)
    buf = io.BytesIO()

    if sound.channels > 1:
        sound = sound.set_channels(1)
    sound.export(buf, format="wav")

    return buf, sound.frame_rate


def upload_blob(bucket_name, source_file, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(source_file)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()


def google_transcribe(video, bucket_name="metamemo"):

    wav_file, frame_rate = convert_to_wav(video)

    # The name of the audio file to transcribe

    bucket_name = "metamemo"
    destination_blob_name = video.file.name

    upload_blob(bucket_name, wav_file, destination_blob_name)

    gcs_uri = "gs://" + bucket_name + "/" + destination_blob_name
    transcript = ""

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=settings.METAMEMO_DEFAULT_LANGUAGE,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(request={"config": config, "audio": audio})
    response = operation.result(timeout=10000)

    for result in response.results:
        transcript += result.alternatives[0].transcript

    delete_blob(bucket_name, destination_blob_name)
    return transcript


def generate_keyword(text):
    max_ngram_size = 1

    kw_extractor = yake.KeywordExtractor(lan=settings.METAMEMO_DEFAULT_LANGUAGE, n=max_ngram_size)

    keywords = kw_extractor.extract_keywords(text)
    return keywords


def save_keywords_qs(queryset):
    for i in queryset:
        text = i.content
        for m in i.medias.all():
            if m.transcription:
                text += m.transcription
        keywords = generate_keyword(text)
        for word, rank in keywords:
            w = MemoKeyWord.objects.get_or_create(word=word)
            i.keyword.add(w[0])


# Action para baixar as midias.
def bulk_download_media(queryset):
    from metamemoapp.tasks import download_async

    for i in queryset:
        if i.mediatype == "VIDEO":
            i.status = "DOWNLOADING"
            i.save()
            download_async.apply_async(kwargs={"url": i.original_url, "mediatype": "VIDEO"})
            print(f"Downloading {i.original_url}")

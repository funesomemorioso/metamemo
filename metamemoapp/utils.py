from django.conf import settings

import io, os, wave
from google.cloud import speech
from google.cloud import storage
from pydub import AudioSegment
import mimetypes
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= getattr(settings, "GOOGLE_APPLICATION_CREDENTIALS", None)
METAMEMO_DEFAULT_LANGUAGE = getattr(settings, "METAMEMO_DEFAULT_LANGUAGE", "pt-BR")

def convert_to_wav(audio_file_name):
    sound = AudioSegment.from_file(audio_file_name)
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

def google_transcribe(audio_file_name, bucket_name='metamemo'):
    
    wav_file, frame_rate = convert_to_wav(audio_file_name)
        
    # The name of the audio file to transcribe
        
    bucket_name = 'metamemo'
    destination_blob_name = os.path.basename(audio_file_name)
    
    upload_blob(bucket_name, wav_file, destination_blob_name)
    
    gcs_uri = 'gs://'+ bucket_name + '/' + destination_blob_name
    transcript = ''
    
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=METAMEMO_DEFAULT_LANGUAGE)

    # Detects speech in the audio file
    operation = client.long_running_recognize(request={"config":config, "audio":audio})
    response = operation.result(timeout=10000)

    for result in response.results:
        transcript += result.alternatives[0].transcript
    
    delete_blob(bucket_name, destination_blob_name)
    return transcript


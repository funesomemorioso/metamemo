from django.db import models
from django.core.files.base import File
import urllib.request
import tempfile, mimetypes
import youtube_dl

# Create your models here.

"""
Aqui você define os modelos de dados, tem uma penca de classes disponíveis para os tipos de dados mais comuns.
Acho que ainda precisa um pente fino e pensar melhor a relação entre MetaMemo e MemoSource.

Hoje eles são basicamente objetos-que-poderiam-ser-strings, mas a ideia é avançar para que isso sirva para gerenciar os
metamemos, coletores e cronjobs.

Depois de modificar o modelo você precisa rodar:
python manage.py makemigrations -> para criar um script de migração dos dados no DB
python mangage.py migrate -> para efetuar as migrações

Obviamente a ideia é fechar o modelo de dados antes de começar a popular o banco definitivamente.
"""

class MemoSource(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return(self.name)

class MetaScraper(models.Model):
    source = models.ForeignKey(MemoSource, on_delete=models.CASCADE)
    url = models.URLField()
    command = models.CharField(max_length=200)
    command_args = models.CharField(max_length=500)

    def __str__(self):
        return(self.source.name)

class MetaMemo(models.Model):
    name = models.CharField(max_length=200)
    scraper = models.ManyToManyField(MetaScraper)

    def __str__(self):
        return(self.name)

class MemoMedia(models.Model):
    STATUS_CHOICES = (
        ('INITIAL', 'Initial'),
        ('DOWNLOADED', 'Downloaded'),
        ('TRANSCRIBED', 'Transcribed'),
        ('READY', 'Ready'),
    )

    original_url = models.URLField(max_length=500)
    original_id = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    transcription = models.TextField(blank=True)
    media = models.FileField(upload_to='metamemo', blank=True) #Add directory by account
    mimetype = models.CharField(max_length=20, blank=True)

    def download_media(self):
        with tempfile.TemporaryDirectory() as tempdirname:
            
            ydl_opts = {
                'outtmpl': f'{tempdirname}/{self.original_id}.%(ext)s',
                'merge_output_format': 'mp4',
                'progress_hooks':[]
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.original_url])
        
            with open(f'{tempdirname}/{self.original_id}.mp4', 'rb') as tmpfile:
                media_file = File(tmpfile)
                result = self.media.save(f"{self.original_id}.mp4", media_file)
                self.status = 'DOWNLOADED'
                #self.mimetype = mimetype
                self.save()
        return True


class MemoItem(models.Model):
    author = models.ForeignKey(MetaMemo, on_delete=models.CASCADE)
    source = models.ForeignKey(MemoSource, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    extraction_date = models.DateTimeField(null=True)
    content_date = models.DateTimeField(null=True)
    url = models.URLField()
    likes = models.IntegerField()
    interactions = models.IntegerField()
    raw = models.JSONField(blank=True, null=True)
    medias = models.ManyToManyField(MemoMedia, blank=True, null=True)
    original_id = models.CharField(max_length=500)

    def __str__(self):
        return(self.title)


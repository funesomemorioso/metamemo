from django.db import models
from django.core.files.base import File
import urllib.request
import tempfile, mimetypes

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
    media = models.FileField(upload_to='media', blank=True) #Add directory by account

    def download_media(self):
        img_temp = tempfile.NamedTemporaryFile(delete=True)
        req = urllib.request.Request(self.original_url)
        with urllib.request.urlopen(req) as response:
            img_temp.write(response.read())
            filename_ext = mimetypes.guess_extension(response.info().get_content_type())
        img_temp.flush()
        filename = self.original_id + filename_ext
        result = self.media.save(filename, File(img_temp))
        self.status = 'DOWNLOADED'
        self.save()
        img_temp.close()
        return result



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


from django.db import models
from django.core.management import call_command

import urllib.request


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


class MemoKeyWord(models.Model):
    word = models.CharField(max_length=200)
    important = models.BooleanField(null=True)

    def __str__(self):
        return(self.word)

class MemoSource(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return(self.name)

class MetaMemo(models.Model):
    name = models.CharField(max_length=200)
    facebook_handle = models.CharField(max_length=200, blank=True)
    instagram_handle = models.CharField(max_length=200, blank=True)
    twitter_handle = models.CharField(max_length=200, blank=True)
    youtube_handle = models.CharField(max_length=200, blank=True)

    def get_facebook(self):
        if self.facebook_handle:
            call_command('import_facebook', username=self.facebook_handle, author=self.name)
    
    def __str__(self):
        return(self.name)

class MemoMedia(models.Model):
    STATUS_CHOICES = (
        ('INITIAL', 'Initial'),
        ('DOWNLOADED', 'Downloaded'),
        ('TRANSCRIBED', 'Transcribed'),
        ('READY', 'Ready'),
        ('QUEUED', 'Queued')
    )

    MEDIATYPE_CHOICES = (
        ('VIDEO', 'Video'),
        ('IMAGE', 'Image'),
    )

    original_url = models.URLField(max_length=500)
    original_id = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    transcription = models.TextField(blank=True)
    media = models.FileField(upload_to='media', blank=True) #Add directory by account
    mediatype = models.CharField(max_length=20, blank=True, choices=MEDIATYPE_CHOICES)

    def __str__(self):
        return self.original_id


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
    shares = models.IntegerField(null=True)
    raw = models.JSONField(blank=True, null=True)
    medias = models.ManyToManyField(MemoMedia, blank=True, null=True)
    original_id = models.CharField(max_length=500)
    keyword = models.ManyToManyField(MemoKeyWord, blank=True, null=True)

    def __str__(self):
        return(self.title)


class MemoContext(models.Model):
    context = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return(self.context)


class MemoNews(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    text = models.TextField(blank=True)
    content_date = models.DateTimeField(null=True)
    source = models.CharField(max_length=200)
    metamemo = models.ForeignKey(MetaMemo, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return(f'{self.title} - {self.source}')
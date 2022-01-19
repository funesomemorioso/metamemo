from django.db import models

# Create your models here.

class MetaMemo(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return(self.name)

class MemoSource(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return(self.name)

class MemoMedia(models.Model):
    url = models.URLField()


class MemoItem(models.Model):
    author = models.ForeignKey(MetaMemo, on_delete=models.CASCADE)
    source = models.ForeignKey(MemoSource, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    extraction_date = models.DateField()
    content_date = models.DateField()
    url = models.URLField()
    likes = models.IntegerField()
    interactions = models.IntegerField()
    raw = models.JSONField(blank=True, null=True)
    medias = models.ManyToManyField(MemoMedia, blank=True, null=True)

    def __str__(self):
        return(self.title)


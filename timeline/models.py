from django.db import models

# Create your models here.
class Timeline(models.Model):
    name = models.CharField(max_length=500)
    text = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return(self.name)
    

class Session(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    text = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

class Fact(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline', blank=True, null=True)
    source = models.CharField(max_length=500, blank=True)
    url = models.URLField(blank=True)
    date = models.DateTimeField()
    

    def __str__(self):
        return(self.text)

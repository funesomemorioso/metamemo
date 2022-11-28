from django.core.management import call_command
from django.db import models

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
        return self.word


class MemoSource(models.Model):
    name = models.CharField(max_length=200)
    cookie = models.FileField(upload_to="source", blank=True, null=True)  # Add directory by account

    def __str__(self):
        return self.name

    def ico(self):
        icons = {
            "Facebook": "face",
            "Youtube": "youtube1",
            "Twitter": "twitter1",
            "Instagram": "instagram1",
            "Telegram": "telegram",
        }
        if self.name in icons:
            return icons[self.name]


class MetaMemo(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="memo", blank=True, null=True)
    facebook_handle = models.CharField(max_length=200, blank=True)
    instagram_handle = models.CharField(max_length=200, blank=True)
    twitter_handle = models.CharField(max_length=200, blank=True)
    youtube_handle = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def get_facebook(self):
        if self.facebook_handle:
            call_command("import_facebook", username=self.facebook_handle, author=self.name)


class MemoMedia(models.Model):
    STATUS_CHOICES = (
        ("INITIAL", "Initial"),
        ("DOWNLOADING", "Downloading"),
        ("DOWNLOADED", "Downloaded"),
        ("FAILED_DOWNLOAD", "Download Failed"),
        ("TRANSCRIBING", "Transcribing"),
        ("TRANSCRIBED", "Transcribed"),
        ("FAILED_TRANSCRIBE", "Transcribe Failed"),
    )

    MEDIATYPE_CHOICES = (
        ("VIDEO", "Video"),
        ("IMAGE", "Image"),
    )

    original_url = models.URLField(max_length=500)
    original_id = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    transcription = models.TextField(blank=True)
    media = models.FileField(upload_to="media", blank=True)  # Add directory by account
    mediatype = models.CharField(max_length=20, blank=True, choices=MEDIATYPE_CHOICES)
    progress = models.FloatField(default=0)
    source = models.ForeignKey(MemoSource, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.original_id


class MemoItemQuerySet(models.QuerySet):
    def get_full(self, pk):
        return self.select_related("author").prefetch_related("medias").get(pk=pk)

    def from_author(self, value):
        if not value:
            return self
        return self.filter(author__name=value).select_related("author")

    def from_authors(self, values):
        if not values:
            return self
        return self.filter(author__name__in=values).select_related("author")

    def from_source(self, value):
        if not value:
            return self
        return self.filter(source__name=value).select_related("source")

    def from_sources(self, values):
        if not values:
            return self
        return self.filter(source__name__in=values).select_related("source")

    def since(self, value):
        if not value:
            return self
        return self.filter(content_date__gte=value)

    def until(self, value):
        if not value:
            return self
        return self.filter(content_date__lte=value)

    def search(self, value):
        if not value:
            return self
        return self.filter(models.Q(content__icontains=value) | models.Q(title__icontains=value))


class MemoItem(models.Model):
    objects = MemoItemQuerySet().as_manager()

    author = models.ForeignKey(MetaMemo, on_delete=models.CASCADE)
    source = models.ForeignKey(MemoSource, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField(blank=True)
    extraction_date = models.DateTimeField(null=True)
    content_date = models.DateTimeField(null=True)
    url = models.URLField()
    likes = models.IntegerField()
    interactions = models.IntegerField()
    shares = models.IntegerField(null=True)
    raw = models.JSONField(blank=True, null=True)
    medias = models.ManyToManyField(MemoMedia, blank=True)
    original_id = models.CharField(max_length=500)
    keyword = models.ManyToManyField(MemoKeyWord, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["content_date"]),
        ]
        ordering = ["-content_date"]

    def serialize(self, full=False):
        video, image = None, None
        for media in self.medias.all():
            if video is None and media.mediatype == "VIDEO":
                video = media
            elif image is None and media.mediatype == "IMAGE":
                image = media

        row = {
            "id": self.id,
            "content_date": self.content_date,
            "likes": self.likes,
            "interactions": self.interactions,
            "shares": self.shares,
            "title": self.title,
            "source": self.source.name,
            "author": self.author.name,
            "url": self.url,
            "video_url": video.original_url if video is not None else None,
            "image_url": image.original_url if image is not None else None,
            "content": self.content,
        }
        if full:
            row["raw"] = self.raw
        return row


class MemoContextQuerySet(models.QuerySet):
    def since(self, value):
        if not value:
            return self
        return self.filter(start_date__gte=value)

    def until(self, value):
        if not value:
            return self
        return self.filter(end_date__lte=value)


class MemoContext(models.Model):
    objects = MemoContextQuerySet().as_manager()

    context = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=500, blank=True, null=True)
    keyword = models.ManyToManyField(MemoKeyWord, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["start_date", "end_date"]),
        ]
        ordering = ["-start_date"]

    def __str__(self):
        return self.context


class MemoNews(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    text = models.TextField(blank=True)
    content_date = models.DateTimeField(null=True)
    source = models.CharField(max_length=200)
    metamemo = models.ForeignKey(MetaMemo, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_date"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.source}"


class NewsSource(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="news", blank=True)

    def __str__(self):
        return self.name


class NewsItemQuerySet(models.QuerySet):
    def since(self, value):
        if not value:
            return self
        return self.filter(content_date__gte=value)

    def until(self, value):
        if not value:
            return self
        return self.filter(content_date__lte=value)


class NewsItem(models.Model):
    objects = NewsItemQuerySet().as_manager()

    title = models.CharField(max_length=200)
    url = models.URLField()
    text = models.TextField(blank=True)
    content_date = models.DateTimeField(null=True)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, null=True)
    metamemo = models.ForeignKey(MetaMemo, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_date"]),
        ]
        ordering = ["-content_date"]

    def __str__(self):
        return f"{self.title} - {self.source}"


class NewsCoverQuerySet(models.QuerySet):
    def since(self, value):
        if not value:
            return self
        return self.filter(content_date__gte=value)

    def until(self, value):
        if not value:
            return self
        return self.filter(content_date__lte=value)


class NewsCover(models.Model):
    objects = NewsCoverQuerySet().as_manager()

    content_date = models.DateTimeField(null=True)
    media = models.ImageField(upload_to="cover", blank=True)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_date"]),
        ]
        ordering = ["-content_date"]

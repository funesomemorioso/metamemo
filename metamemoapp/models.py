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

import django.contrib.postgres.indexes as pg_indexes
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField
from django.core.management import call_command
from django.db import connection, models


class SearchQuerySetMixin:
    def search(self, term):
        qs = self

        if term:
            query = SearchQuery(term, config="pg_catalog.portuguese", search_type="websearch")
            qs = qs.annotate(search_rank=SearchRank(models.F("search_data"), query)).filter(search_data=query)
            # Overwriting `qs.query.order_by` to APPEND ordering field
            # instead of OVERWRITTING (as in `qs.order_by`). We append directly
            # (instead of using `qs.query.add_ordering` because the search rank
            # must have precedence over the other ordering.
            qs.query.order_by = tuple(["-search_rank"] + list(qs.query.order_by))
        return qs

    def order_by(self, *args, **kwargs):
        # We must force search_rank ordering, since some operations will add
        # ordering after calling `.search` (like in Django Admin)
        qs = super().order_by(*args, **kwargs)
        if "-search_rank" in qs.query.order_by and qs.query.order_by[0] != "-search_rank":
            qs.query.order_by = tuple(["-search_rank"] + [item for item in qs.query.order_by if item != "-search_rank"])
        return qs


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

class MemoMediaQuerySet(SearchQuerySetMixin, models.QuerySet):
    def from_source(self, value):
        qs = self.select_related("source")
        if not value:
            return qs
        return qs.filter(source__name=value)

    def from_sources(self, values):
        qs = self.select_related("source")
        if not values:
            return qs
        return qs.filter(source__name__in=values)


class MemoMedia(models.Model):
    objects = MemoMediaQuerySet().as_manager()

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
    search_data = SearchVectorField(null=True)

    class Meta:
        indexes = [
            pg_indexes.GinIndex(fields=["search_data"]),
        ]

    def __str__(self):
        return self.original_id

    def serialize(self, full=False):
        return {
            "source": self.source.name,
            "original_id": self.original_id,
            "original_url": self.original_url,
            "status": self.status,
            "media_url": self.media.url if self.media else None,
            "mediatype": self.mediatype,
            "progress": self.progress,
            "transcription": self.transcription,
        }


class MemoItemQuerySet(SearchQuerySetMixin, models.QuerySet):
    def get_full(self, pk):
        return self.select_related("author").prefetch_related("medias").get(pk=pk)

    def from_author(self, value):
        qs = self.select_related("author")
        if not value:
            return qs
        return qs.filter(author__name=value)

    def from_authors(self, values):
        qs = self.select_related("author")
        if not values:
            return qs
        return qs.filter(author__name__in=values)

    def from_source(self, value):
        qs = self.select_related("source")
        if not value:
            return qs
        return qs.filter(source__name=value)

    def from_sources(self, values):
        qs = self.select_related("source")
        if not values:
            return qs
        return qs.filter(source__name__in=values)

    def since(self, value):
        if not value:
            return self
        return self.filter(content_date__gte=value)

    def until(self, value):
        if not value:
            return self
        return self.filter(content_date__lte=value)

    def export_csv(self):
        sql = """
            WITH medias AS (
            SELECT
                u.memoitem_id,
                m.media,
                m.original_url,
                m.mediatype
            FROM (
                SELECT
                i.memoitem_id,
                m.mediatype,
                MIN(i.memomedia_id) AS memomedia_id
                FROM metamemoapp_memoitem_medias AS i
                LEFT JOIN metamemoapp_memomedia AS m
                    ON m.id = i.memomedia_id
                WHERE m.media IS NOT NULL
                GROUP BY i.memoitem_id, m.mediatype
            ) AS u
                LEFT JOIN metamemoapp_memomedia AS m ON
                u.memomedia_id = m.id
                AND u.mediatype = m.mediatype
            ),
            images AS (
            SELECT memoitem_id, media, original_url
            FROM medias
            WHERE mediatype = 'IMAGE'
            ),
            videos AS (
            SELECT memoitem_id, media, original_url
            FROM medias
            WHERE mediatype = 'VIDEO'
            )
            SELECT
            i.id,
            i.content_date,
            a.name AS author,
            s.name AS source,
            i.likes,
            i.interactions,
            i.shares,
            i.original_id,
            i.url,
            i.title,
            CASE
                WHEN mv.media IS NOT NULL THEN 'downloaded'
                WHEN mv.memoitem_id IS NOT NULL THEN 'not_downloaded'
                ELSE 'no_media'
            END AS video_status,
            mv.media AS video_internal_url,
            mv.original_url AS video_original_url,
            CASE
                WHEN mi.media IS NOT NULL THEN 'downloaded'
                WHEN mi.memoitem_id IS NOT NULL THEN 'not_downloaded'
                ELSE 'no_media'
            END AS image_status,
            mi.media AS image_internal_url,
            mi.original_url AS image_original_url,
            i.content
            FROM metamemoapp_memoitem AS i
            LEFT JOIN videos AS mv
                ON mv.memoitem_id = i.id
            LEFT JOIN images AS mi
                ON mi.memoitem_id = i.id
            LEFT JOIN metamemoapp_metamemo AS a
                ON a.id = i.author_id
            LEFT JOIN metamemoapp_memosource AS s
                ON s.id = i.source_id
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            yield [item[0] for item in cursor.description]  # Header
            for row in cursor.fetchall():
                yield row


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
    search_data = SearchVectorField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["content_date"]),
            pg_indexes.GinIndex(fields=["search_data"]),
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
            "keywords": ", ".join(keyword.word for keyword in self.keyword.all()),
        }
        if full:
            row["raw"] = self.raw
        return row


class MemoContextQuerySet(SearchQuerySetMixin, models.QuerySet):
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
    search_data = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["start_date", "end_date"]),
            pg_indexes.GinIndex(fields=["search_data"]),
        ]
        ordering = ["-start_date"]

    def __str__(self):
        return self.context

    def serialize(self, full=False):
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "url": self.url,
            "source": self.source,
            "keywords": ", ".join(keyword.word for keyword in self.keyword.all()),
            "context": self.context,
        }


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


class NewsItemQuerySet(SearchQuerySetMixin, models.QuerySet):
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
    search_data = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_date"]),
            pg_indexes.GinIndex(fields=["search_data"]),
        ]
        ordering = ["-content_date"]

    def __str__(self):
        return f"{self.title} - {self.source}"

    def serialize(self, full=False):
        return {
            "title": self.title,
            "url": self.url,
            "text": self.text,
            "content_date": self.content_date,
            "source": self.source.name,
            "metamemo": self.metamemo.name,
        }


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

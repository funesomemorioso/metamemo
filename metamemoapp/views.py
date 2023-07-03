import csv
import datetime
from pathlib import Path

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone

from metamemoapp import models
from metamemoapp import tasks

DEFAULT_TIMEZONE = timezone.get_default_timezone()
SOCIAL_MEDIA_LIST = ["Facebook", "Twitter", "Youtube", "Instagram", "Telegram", "Blog"]


def bad_request(request, message=None, status=400):
    return render(request, "content/oops.html", {"message": message}, status=status)

def get_metamemos():
    return models.MetaMemo.objects.all()

def get_news_sources():
    return {
        source.name: source.image.url if source.image else None
        for source in models.NewsSource.objects.all()
    }



def queryset_to_lines(qs):
    header = None
    # XXX: we may want to use .iterator() in the future (if the number of rows
    # increases a lot), but we'll need to deal with the timeout, since
    # .iterator() will be a lot slower (but won't use too much memory and will
    # start the response sooner).
    for obj in qs:
        row = obj.serialize()
        if header is None:
            header = list(row.keys())
            yield header
        yield [row.get(field) for field in header]


class Echo:
    """Implements just the write method of the file-like interface"""

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def csv_streaming_response(lines, filename):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(line) for line in lines),
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def json_response(queryset, page=1, page_size=10, full=False):
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    items = [obj.serialize(full=full) for obj in page_obj]
    return JsonResponse({
        "items": items,
        "page": page_obj.number,
        "page_size": page_size,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
    })


def define_pages(page, last_page):
    if page == 1:
        return list(range(page, min(last_page, page + 3)))
    elif page == last_page:
        return list(range(max(1, page - 2), page + 1))
    else:
        return list(range(page - 1, page + 2))


def parse_date(value):
    return datetime.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=DEFAULT_TIMEZONE)


def serialize_queryset(request, output_format, queryset, filename):
    output_format = str(output_format or "").lower().strip()
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    if output_format == "csv":
        return csv_streaming_response(
            lines=queryset_to_lines(queryset),
            filename=filename,
        )
    elif output_format == "json":
        return json_response(queryset, full=True, page=page, page_size=page_size)
    else:
        return bad_request(request, f"Formato de arquivo inválido: {output_format}")


# TODO: order all paginated results
class QueryStringParser:
    def __init__(self, data):
        self._data = data

    def _parse_value(self, type, value, default=None):
        if value is None:
            return default
        elif type is str:
            return str(value)
        elif type is int:
            return int(value)
        elif type is datetime.date:
            return parse_date(value)
        else:
            raise ValueError(f"Unknown type to parse: {type}")

    def str(self, key, default=None):
        return self._data.get(key, default=default)

    def int(self, key, default=None):
        return self._parse_value(int, self._data.get(key), default=default)

    def date(self, key, default=None):
        return self._parse_value(datetime.date, self._data.get(key), default=default)

    def list(self, key, type=str):
        return [self._parse_value(type, value) for value in self._data.getlist(key)]


# MemoItem search/filter form (HTML)
def home(request):
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=7)
    tags = {}  # TODO: implement (from keywords)?
    context = {
        "end_date": end_date,
        "metamemo": get_metamemos(),
        "social_media_list": SOCIAL_MEDIA_LIST,
        "start_date": start_date,
        "tags": tags,
    }
    return render(request, "home.html", context)


# "Static" pages content (HTML)
def content(request, page):
    app_dir = Path(models.__file__).parent
    template_html = f"content/{page}.html"
    filename = app_dir / "templates" / template_html
    if not filename.exists():
        return bad_request(request, message="Página não encontrada", status=404)

    return render(request, template_html)


# NewsItem list (filtered + pagination; HTML, CSV or JSON)
def news_list(request):
    qs = QueryStringParser(request.GET)
    try:
        authors = qs.list("author", type=str)
        content = qs.str("content")
        end_date = qs.date("end_date")
        output_format = qs.str("format")
        page = qs.int("page", default=1)
        sources = qs.list("source", type=str)
        start_date = qs.date("start_date")
        # TODO: pass form data
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    queryset = models.NewsItem.objects.since(start_date).until(end_date).search(content).select_related("source")
    if output_format:
        # TODO: what if `page` is specified?
        return serialize_queryset(
            request,
            output_format,
            queryset,
            filename="metamemo-newsitem-filtered.csv",
        )

    sources_total = {
        source["source__name"]: source["total"]
        for source in queryset.values("source__name").annotate(total=Count("source__name")).order_by("total")
    }
    sources = get_news_sources()
    items = Paginator(queryset, settings.PAGE_SIZE)
    data = {
        "authors": authors,
        "dates": (start_date, end_date),
        "items": items.page(page),
        "metamemo": get_metamemos(),
        "page": page,
        "paginator_list": define_pages(page, items.num_pages),
        "path": request.resolver_match.url_name,
        "results_total": items.count,
        "social_media_list": SOCIAL_MEDIA_LIST,
        "sources": sources,
        "sources_total": sources_total,
        "total_pages": items.num_pages,
    }
    return render(request, "news.html", {"data": data})


# NewsItem detail (HTML)
def news_detail(request, item_id):
    item = models.NewsItem.objects.get(pk=item_id)
    return render(request, "newsitem.html", {"item": item})


# MemoContext list (filtered + pagination; HTML, CSV or JSON)
def contexts(request):
    qs = QueryStringParser(request.GET)
    try:
        authors = qs.list("author", type=str)
        content = qs.str("content")
        end_date = qs.date("end_date")
        output_format = qs.str("format")
        page = qs.int("page", default=1)
        sources = qs.list("source", type=str)
        start_date = qs.date("start_date")
        # TODO: pass form data
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    queryset = models.MemoContext.objects.since(start_date).until(end_date).search(content).prefetch_related("keyword")
    if output_format:
        # TODO: what if `page` is specified?
        return serialize_queryset(
            request,
            output_format,
            queryset,
            filename="metamemo-memocontext-filtered.csv",
        )
    sources = get_news_sources()
    items = Paginator(queryset, settings.PAGE_SIZE)
    data = {
        "dates": (start_date, end_date),
        "items": items.get_page(page),
        "metamemo": get_metamemos(),
        "page": page,
        "paginator_list": define_pages(page, items.num_pages),
        "path": request.resolver_match.url_name,
        "results_total": items.count,
        "social_media_list": SOCIAL_MEDIA_LIST,
        "sources": sources,
        "total_pages": items.num_pages,
    }
    return render(request, "contexts.html", {"data": data})


# NewsCover list (filtered + pagination; HTML, CSV or JSON)
def news_covers(request):
    qs = QueryStringParser(request.GET)
    try:
        authors = qs.list("author", type=str)
        content = qs.str("content")
        end_date = qs.date("end_date")
        output_format = qs.str("format")
        page = qs.int("page", default=1)
        sources = qs.list("source", type=str)
        start_date = qs.date("start_date")
        # TODO: pass form data
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    queryset = models.NewsCover.objects.since(start_date).until(end_date).select_related("source")
    if output_format:
        # TODO: what if `page` is specified?
        return serialize_queryset(
            request,
            output_format,
            queryset,
            filename="metamemo-newscover-filtered.csv",
        )
    sources = get_news_sources()
    items = Paginator(queryset, settings.PAGE_SIZE)
    data = {
        "dates": (start_date, end_date),
        "items": items.get_page(page),
        "metamemo": get_metamemos(),
        "page": page,
        "paginator_list": define_pages(page, items.num_pages),
        "path": request.resolver_match.url_name,
        "results_total": items.count,
        "social_media_list": SOCIAL_MEDIA_LIST,
        "sources": sources,
        "total_pages": items.num_pages,
    }
    return render(request, "newscovers.html", {"data": data})


# MemoItem list (filtered + pagination; HTML, CSV or JSON)
def lista(request):
    qs = QueryStringParser(request.GET)
    try:
        authors = qs.list("author", type=str)
        content = qs.str("content")
        end_date = qs.date("end_date")
        output_format = qs.str("format")
        page = qs.int("page", default=1)
        sources = qs.list("source", type=str)
        start_date = qs.date("start_date")
        # TODO: pass form data
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    queryset = (
        models.MemoItem.objects.since(start_date)
        .until(end_date)
        .from_authors(authors)
        .from_sources(sources)
        .search(content)
        .prefetch_related("medias", "keyword")
    )

    if output_format:
        # TODO: what if `page` is specified?
        return serialize_queryset(
            request,
            output_format,
            queryset,
            filename="metamemo-memoitems-filtered.csv",
        )

    items = Paginator(queryset, settings.PAGE_SIZE)
    data = {
        "authors": authors,
        "content": content,
        "dates": (start_date, end_date),
        "items": items.get_page(page),
        "metamemo": get_metamemos(),
        "page": page,
        "paginator_list": define_pages(page, items.num_pages),
        "path": request.resolver_match.url_name,
        "results_total": items.count,
        "social_media_list": SOCIAL_MEDIA_LIST,
        "sources": sources,
        "sources_total": {},  # TODO: what to do?
        "total_pages": items.num_pages,
    }
    return render(request, "files.html", {"data": data})


# MemoItem detail (HTML)
def memoitem(request, item_id):
    memoitem = models.MemoItem.objects.get_full(pk=item_id)
    return render(request, "memoitem.html", {"memoitem": memoitem})


# MemoItem (whole database) download (CSV)
def memoitems_download(request):
    return csv_streaming_response(
        lines=models.MemoItem.objects.export_csv(),
        filename=f"metamemo-memoitems-{timezone.now().date()}.csv",
    )


# MemoMedia list (filtered + pagination; HTML, CSV or JSON)
def media_list(request):
    qs = QueryStringParser(request.GET)
    try:
        authors = qs.list("author", type=str)
        content = qs.str("content")
        end_date = qs.date("end_date")
        output_format = qs.str("format")
        page = qs.int("page", default=1)
        sources = qs.list("source", type=str)
        start_date = qs.date("start_date")
        # TODO: pass form data
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    queryset = (
        models.MemoMedia.objects
        .filter(~Q(transcription=""), transcription__isnull=False)
        .from_sources(sources)
        .search(content)
        .filter(memoitem__author__name__in=authors)
        .select_related("source")
        .prefetch_related("memoitem_set", "memoitem_set__source", "memoitem_set__author")
    )


    if output_format:
        # TODO: what if `page` is specified?
        return serialize_queryset(
            request,
            output_format,
            queryset,
            filename="metamemo-memomedia-filtered.csv",
        )

    items = Paginator(queryset, settings.PAGE_SIZE)
    objs = []
    for obj in items.get_page(page):
        obj.excerpt = models.snippet(obj.transcription, content)
        obj.memoitem = obj.memoitem_set.first()
        objs.append(obj)
    data = {
        "content": content,
        "items": objs,
        "metamemo": get_metamemos(),
        "page": page,
        "paginator_list": define_pages(page, items.num_pages),
        "path": request.resolver_match.url_name,
        "results_total": items.count,
        "social_media_list": SOCIAL_MEDIA_LIST,
        "sources": sources,
        "total_pages": items.num_pages,
    }
    return render(request, "media.html", {"data": data})


# MemoMedia download start task (API)
def get_media(request, item_id):
    memoitem = models.MemoItem.objects.get_full(pk=item_id)

    response = {"medias": []}
    for p in memoitem.medias.all():
        if p.mediatype == "VIDEO" and p.status in ["INITIAL", "FAILED_DOWNLOAD"]:
            p.status = "DOWNLOADING"
            p.save(update_fields=["status"])
            tasks.download_async.apply_async(kwargs={"url": p.original_url, "mediatype": "VIDEO"}, queue="fastlane")
        elif p.mediatype == "IMAGE" and p.status in ["INITIAL", "FAILED_DOWNLOAD"]:
            p.status = "DOWNLOADING"
            p.save(update_fields=["status"])
            tasks.download_img_async.apply_async(kwargs={"url": p.original_url, "pk": p.pk}, queue="fastlane")
        response["medias"].append({"mediatype": p.mediatype, "original_url": p.original_url, "status": p.status})
    return JsonResponse(response, status=200)

import csv
import datetime

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone

from metamemoapp.models import MemoContext, MemoItem, MetaMemo, NewsCover, NewsItem, NewsSource
from metamemoapp.tasks import download_async, download_img_async

DEFAULT_TIMEZONE = timezone.get_default_timezone()


def bad_request(request, message=None):
    return render(request, "content/oops.html", {"message": message}, status=400)


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


def json_response(queryset, full=False):
    return JsonResponse({"items": [obj.serialize(full=full) for obj in queryset]})


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
    if output_format == "csv":
        return csv_streaming_response(
            lines=queryset_to_lines(queryset),
            filename=filename,
        )
    elif output_format == "json":
        return json_response(queryset, full=True)
    else:
        return bad_request(request, f"Formato de arquivo inválido: {output_format}")


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
    metamemo = MetaMemo.objects.all()
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=7)
    tags = {}  # TODO: implement (from keywords)?
    context = {"metamemo": metamemo, "end_date": end_date, "start_date": start_date, "tags": tags}
    return render(request, "home.html", context)


# "Static" pages content (HTML)
def content(request, page):
    return render(request, f"content/{page}.html")


# NewsItem list (filtered + pagination; HTML, CSV or JSON)
def news_list(request):
    qs = QueryStringParser(request.GET)
    try:
        content = qs.str("content")
        end_date = qs.date("end_date")
        output_format = qs.str("format")
        page = qs.int("page", default=1)
        start_date = qs.date("start_date")
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    queryset = NewsItem.objects.since(start_date).until(end_date).search(content)
    if output_format:
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
    sources = {source.name: source.image.url if source.image else None for source in NewsSource.objects.all()}
    items = Paginator(queryset, settings.PAGE_SIZE)
    data = {
        "path": request.resolver_match.url_name,
        "dates": (start_date, end_date),
        "paginator_list": define_pages(page, items.num_pages),
        "items": items.page(page),
        "results_total": items.count,
        "sources": sources,
        "sources_total": sources_total,
    }
    return render(request, "news.html", {"data": data})


# NewsItem detail (HTML)
def news_detail(request, item_id):
    item = NewsItem.objects.get(pk=item_id)
    return render(request, "newsitem.html", {"item": item})


# MemoContext list (filtered; HTML, CSV or JSON) + NewsCover list (filtered + pagination; HTML)
def contexts(request):
    qs = QueryStringParser(request.GET)
    try:
        content = qs.str("content")
        end_date = qs.date("end_date")
        output_format = qs.str("format")
        page = qs.int("page", default=1)
        start_date = qs.date("start_date")
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    memocontext = MemoContext.objects.since(start_date).until(end_date).search(content).prefetch_related("keyword")
    if output_format:
        return serialize_queryset(
            request,
            output_format,
            memocontext,
            filename="metamemo-memocontext-filtered.csv",
        )
    newscovers = NewsCover.objects.since(start_date).until(end_date).select_related("source")
    sources = {source.name: source.image.url if source.image else None for source in NewsSource.objects.all()}
    items = Paginator(newscovers, settings.PAGE_SIZE)
    data = {
        "path": request.resolver_match.url_name,
        "sources": sources,
        "dates": (start_date, end_date),
        "paginator_list": define_pages(page, items.num_pages),
        "items": items.get_page(page),
        "memocontexts": memocontext,
        "results_total": items.count,
    }
    return render(request, "contexts.html", {"data": data})


# MemoItem list (filtered + pagination; HTML, CSV or JSON)
def lista(request):
    qs = QueryStringParser(request.GET)
    try:
        page = qs.int("page", default=1)
        output_format = qs.str("format")
        content = qs.str("content")
        authors = qs.list("author", type=str)
        sources = qs.list("source", type=str)
        start_date = qs.date("start_date")
        end_date = qs.date("end_date")
    except ValueError:
        return bad_request(request, message="Erro de formato nos filtros")

    queryset = (
        MemoItem.objects.since(start_date)
        .until(end_date)
        .from_authors(authors)
        .from_sources(sources)
        .search(content)
        .prefetch_related("medias", "keyword")
    )

    if output_format:
        return serialize_queryset(
            request,
            output_format,
            queryset,
            filename="metamemo-memoitems-filtered.csv",
        )

    items = Paginator(queryset, settings.PAGE_SIZE)
    data = {
        "path": request.resolver_match.url_name,
        "dates": (start_date, end_date),
        "paginator_list": define_pages(page, items.num_pages),
        "items": items.get_page(page),
        "results_total": items.count,
        "social_sources": {
            "Facebook": "face",
            "Twitter": "twitter1",
            "Youtube": "youtube1",
            "Instagram": "instagram1",
            "Telegram": "telegram",
            "Blog": "blog1",
        },
        "sources_total": {},  # TODO: what to do?
        "page": page,
        "content": content,
        "authors": authors,
        "sources": sources,
    }
    return render(request, "files.html", {"data": data})


# MemoItem detail (HTML)
def memoitem(request, item_id):
    memoitem = MemoItem.objects.get_full(pk=item_id)
    return render(request, "memoitem.html", {"memoitem": memoitem})


# MemoItem (whole database) download (CSV)
def memoitems_download(request):
    return csv_streaming_response(
        lines=MemoItem.objects.export_csv(),
        filename=f"metamemo-memoitems-{timezone.now().date()}.csv",
    )


# MemoMedia download start task (API)
def get_media(request, item_id):
    memoitem = MemoItem.objects.get_full(pk=item_id)

    response = {"medias": []}
    for p in memoitem.medias.all():
        if p.mediatype == "VIDEO" and p.status in ["INITIAL", "FAILED_DOWNLOAD"]:
            p.status = "DOWNLOADING"
            p.save(update_fields=["status"])
            download_async.apply_async(kwargs={"url": p.original_url, "mediatype": "VIDEO"}, queue="fastlane")
        elif p.mediatype == "IMAGE" and p.status in ["INITIAL", "FAILED_DOWNLOAD"]:
            p.status = "DOWNLOADING"
            p.save(update_fields=["status"])
            download_img_async.apply_async(kwargs={"url": p.original_url, "pk": p.pk}, queue="fastlane")
        response["medias"].append({"mediatype": p.mediatype, "original_url": p.original_url, "status": p.status})
    return JsonResponse(response, status=200)

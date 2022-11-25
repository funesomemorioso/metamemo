import csv
import datetime

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from metamemoapp.models import MemoContext, MemoItem, MetaMemo, NewsCover, NewsItem, NewsSource
from metamemoapp.tasks import download_async, download_img_async

DEFAULT_TIMEZONE = timezone.get_default_timezone()


def bad_request(request):
    return render(request, "content/oops.html", status=400)


def define_pages(page, last_page):
    if page == 1:
        return list(range(page, min(last_page, page + 3)))
    elif page == last_page:
        return list(range(max(1, page - 2), page + 1))
    else:
        return list(range(page - 1, page + 2))


def parse_date(value):
    return datetime.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=DEFAULT_TIMEZONE)


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


def home(request):
    metamemo = MetaMemo.objects.all()
    last_date = timezone.now().date()
    first_date = last_date - datetime.timedelta(days=7)
    context = {"metamemo": metamemo, "y_date": last_date, "date": first_date, "tags": tags}
    tags = {}  # TODO: implement (from keywords)?
    return render(request, "home.html", context)


def news(request):
    qs = QueryStringParser(request.GET)
    try:
        page = qs.int("page", default=1)
        start_date = qs.date("start_date")
        end_date = qs.date("end_date")
    except ValueError:
        return bad_request(request)

    queryset = NewsItem.objects.since(start_date).until(end_date)
    sources_total = {
        source["source__name"]: source["total"]
        for source in queryset.values("source__name").annotate(total=Count("source__name")).order_by("total")
    }
    sources = {
        source.name: source.image.url if source.image else None
        for source in NewsSource.objects.all()
    }
    items = Paginator(queryset, 50)
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


def contexts(request):
    qs = QueryStringParser(request.GET)
    try:
        page = qs.int("page", default=1)
        start_date = qs.date("start_date")
        end_date = qs.date("end_date")
    except ValueError:
        return bad_request(request)

    memocontext = MemoContext.objects.since(start_date).until(end_date)
    newscovers = NewsCover.objects.since(start_date).until(end_date)
    sources = {source.name: source.image.url if source.image else None for source in NewsSource.objects.all()}
    items = Paginator(newscovers.qs, 50)
    data = {
        "path": request.resolver_match.url_name,
        "sources": sources,
        "dates": (start_date, end_date),
        "paginator_list": define_pages(page, items.num_pages),
        "items": items.get_page(page),
        "memocontexts": memocontext.qs,
        "results_total": items.count,
    }
    return render(request, "contexts.html", {"data": data})


def lista(request):
    qs = QueryStringParser(request.GET)
    try:
        page = qs.int("page", default=1)
        content = qs.str("content")
        authors = qs.list("author", type=str)
        sources = qs.list("source", type=str)
        start_date = qs.date("start_date")
        end_date = qs.date("end_date")
    except ValueError:
        return bad_request(request)

    queryset = (
        MemoItem.objects
        .since(start_date).until(end_date)
        .from_authors(authors).from_sources(sources)
        .search(content)
        .prefetch_related("medias")
    )


    items = Paginator(queryset, 50)
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
    }
    return render(request, "files.html", {"data": data})


def memoitem(request, item_id):
    memoitem = MemoItem.objects.get_full(pk=item_id)
    return render(request, "memoitem.html", {"memoitem": memoitem})


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


def content(request, page):
    return render(request, f"content/{page}.html")

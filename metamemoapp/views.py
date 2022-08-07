from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from metamemoapp.models import (
    MetaMemo,
    MemoItem,
    MemoContext,
    MemoNews,
    NewsSource,
    NewsCover,
    NewsItem,
)
from metamemoapp.filters import MemoItemFilter, MemoNewsFilter, MemoContextFilter, NewsCoverFilter
from django.core.paginator import Paginator
from django.db.models import Count, Q


from datetime import date, datetime, timedelta
from collections import Counter
from metamemoapp.tasks import download_async, download_img_async

# Create your views here.
def home(request):
    metamemo = MetaMemo.objects.all()
    #tags = MemoItem.objects.all().values_list("keyword__word", flat=True)
    #tags = Counter(tags)
    #tags[None] = 0
    tags = {}
    data_atual = datetime.now() 
    data_ontem = data_atual - timedelta(days=1)
    return render(
        request, "home.html", {
            "metamemo": metamemo,
            "y_date":data_ontem,
            "date":data_atual, 
            "tags": tags
            })


def news(request):
    newsfilter = MemoNewsFilter(request.GET, queryset=NewsItem.objects.all().order_by("-content_date"))

    sources_total = {
        source["source__name"]: source["total"]
        for source in newsfilter.qs.values("source__name")
        .annotate(total=Count("source__name"))
        .order_by("total")
    }

    sources = {
        source.name: source.image.url if source.image else None
        for source in NewsSource.objects.all()
    }

    items = Paginator(newsfilter.qs, 50)

    try:
        page_nm = int(request.GET.get("page", 1))
    except ValueError:
        page_nm = 1
    last_page = items.num_pages

    if page_nm == 1:
        pages = list(range(page_nm, min(last_page, page_nm + 3)))
    elif page_nm == items.num_pages:
        pages = list(range(max(1, page_nm - 2), page_nm + 1))
    else:
        pages = list(range(page_nm - 1, page_nm + 2))

    dates = (request.GET.get("start_date"), request.GET.get("end_date"))

    data = {
        "path": request.resolver_match.url_name,
        "dates": dates,
        "paginator_list": pages,
        "items": items.page(page_nm),
        "results_total": items.count,
        "sources": sources,
        "sources_total": sources_total,
    }

    return render(request, "news.html", {"data": data})


def parse_date(string):
    try:
        return date(*[int(piece) for piece in string.split("-")])
    except (ValueError, AttributeError):
        return None


def contexts(request):
    dates = (request.GET.get("start_date"), request.GET.get("end_date"))

    memocontext = MemoContextFilter(
        request.GET,
        queryset=MemoContext.objects.all().order_by("-start_date"),
    )

    newscovers = NewsCoverFilter(
        request.GET,
        queryset=NewsCover.objects.all().order_by("-content_date"),
    )

    items = Paginator(newscovers.qs, 50)

    try:
        page_nm = int(request.GET.get("page", 1))
    except ValueError:
        page_nm = 1
    last_page = items.num_pages

    if page_nm == 1:
        pages = list(range(page_nm, min(last_page, page_nm + 3)))
    elif page_nm == items.num_pages:
        pages = list(range(max(1, page_nm - 2), page_nm + 1))
    else:
        pages = list(range(page_nm - 1, page_nm + 2))

    sources = {
        source.name: source.image.url if source.image else None
        for source in NewsSource.objects.all()
    }

    data = {
        "path": request.resolver_match.url_name,
        "sources": sources,
        "dates": dates,
        "paginator_list": pages,
        "items": items.get_page(page_nm),
        "memocontexts": memocontext.qs,
        "results_total": items.count,
    }

    return render(request, "contexts.html", {"data": data})


def lista(request):
    metamemo = MetaMemo.objects.all()

    social_sources = {
        "Facebook": "face",
        "Twitter": "twitter1",
        "Youtube": "youtube1",
        "Instagram": "instagram1",
        "Telegram": "telegram",
        "Blog": "blog1",
    }

    #memoqs = 
    memofilter = MemoItemFilter(
        request.GET,
        queryset=MemoItem.objects.all().order_by("-content_date"),
    )

    #sources_total = {
    #    source["source__name"]: source["total"]
    #    for source in memofilter.qs.values("source__name")
    #    .annotate(total=Count("source__name"))
    #    .order_by("total")
    #}

    items = Paginator(memofilter.qs.prefetch_related("medias").select_related("author", "source"), 50)
    
    try:
        page_nm = int(request.GET.get("page", 1))
    except ValueError:
        page_nm = 1
    last_page = items.num_pages

    if page_nm == 1:
        pages = list(range(page_nm, min(last_page, page_nm + 3)))
    elif page_nm == items.num_pages:
        pages = list(range(max(1, page_nm - 2), page_nm + 1))
    else:
        pages = list(range(page_nm - 1, page_nm + 2))

    # ToDo: Implementar tags
    #tags_g = {}
    #tags_raw = memofilter.qs.values_list("keyword__word", flat=True)
    #tags_g = Counter(tags_raw)
    #tags_g[None] = 0
    #tags = tags_g.most_common(10)
    
    dates = (request.GET.get("start_date"), request.GET.get("end_date"))

    data = {
        "path": request.resolver_match.url_name,
        "dates": dates,
        "paginator_list": pages,
        "items": items.get_page(page_nm),
        "results_total": items.count,
        "social_sources": social_sources,
        "sources_total": [],#sources_total,
        #"metamemo": metamemo,
        #"tags": tags,
    }

    return render(request, "files.html", {"data": data})


def memoitem(request, item_id):
    memoitem = MemoItem.objects.get(pk=item_id)
    return render(request, "memoitem.html", {"memoitem": memoitem})


def get_media(request, item_id):
    memoitem = MemoItem.objects.get(pk=item_id)

    response = {
        "medias": [],
    }
    for p in memoitem.medias.all():
        if p.mediatype == "VIDEO" and p.status in ["INITIAL", "FAILED_DOWNLOAD"]:
            p.status = "DOWNLOADING"
            p.save(
                update_fields=[
                    "status",
                ]
            )
            download_async.apply_async(
                kwargs={"url": p.original_url, "mediatype": "VIDEO"}, queue="fastlane"
            )
        elif p.mediatype == "IMAGE" and p.status in ["INITIAL", "FAILED_DOWNLOAD"]:
            p.status = "DOWNLOADING"
            p.save(
                update_fields=[
                    "status",
                ]
            )
            download_img_async.apply_async(
                kwargs={"url": p.original_url, "pk": p.pk}, queue="fastlane"
            )
        response["medias"].append(
            {
                "mediatype": p.mediatype,
                "original_url": p.original_url,
                "status": p.status,
            }
        )
    return JsonResponse(response, status=200)


def content(request, page):
    return render(request, f"content/{page}.html")

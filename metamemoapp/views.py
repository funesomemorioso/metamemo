from django.shortcuts import render
from metamemoapp.models import MetaMemo, MemoItem, MemoContext, MemoNews
from datetime import datetime
# Create your views here.
def index(request):
    metamemo_list = MetaMemo.objects.all()
    return render(request, 'index.html', {'metamemo_list': metamemo_list})


def list(request, day=datetime.now().day, month=datetime.now().month, year=datetime.now().year):
    d = datetime(year, month,day)
    memoitem_list = MemoItem.objects.filter(content_date__day=day,content_date__month=month,content_date__year=year)
    memocontext_list = MemoContext.objects.filter(start_date__day__lte=day,start_date__month__lte=month,start_date__year__lte=year, end_date__day__gte=day,end_date__month__gte=month,end_date__year__gte=year)
    memonews_list = MemoNews.objects.filter(content_date__day=day,content_date__month=month,content_date__year=year)

    return render(request, 'list.html', {'date':d, 'memoitem_list': memoitem_list, 'memocontext_list': memocontext_list, 'memonews_list':memonews_list})
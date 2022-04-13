from django.http import HttpResponse
from django.shortcuts import render
from metamemoapp.models import MetaMemo, MemoItem, MemoContext, MemoNews
from metamemoapp.filters import MemoItemFilter, MemoNewsFilter
from django.core.paginator import Paginator

from datetime import datetime, timedelta
from collections import Counter

# Create your views here.
def index(request):
    metamemo_list = MetaMemo.objects.all()
    data = {
        'social_list' : {},
    }
    return render(request, 'index.html', {'metamemo_list': metamemo_list, 'data': data})

def list(request):

    #author=request.GET['author']

    memofilter = MemoItemFilter(request.GET, queryset=MemoItem.objects.all().order_by('content_date'))
    newsfilter = MemoNewsFilter(request.GET, queryset=MemoNews.objects.all().order_by('content_date'))
    memoitem = Paginator(memofilter.qs, 25)
    memonews = Paginator(newsfilter.qs, 3)
    print(memofilter.get_filters()['date__end'])

    #Hackish
    tags = {}
    tags_raw = memofilter.qs.values_list('keyword__word', flat=True)
    tags = Counter(tags_raw)
    tags[None]=0
    
    data = {
        'memofilter' : memofilter,
        'metamemo' : MetaMemo.objects.all(),
        'memoitem' : memoitem.page(1),
        'memonews' : memonews.page(1),
        'tags' : tags.most_common(10)
    }
    
    return render(request, 'list.html', {'data' : data})

def integra(request, item_id):
    
    memoitem = MemoItem.objects.get(pk=item_id)
    print(str(memoitem))
    data = {
        'social_list' : {},
        'memoitem': memoitem,   
        'item_id': item_id
    }
    return render(request, 'integra.html', {'data': data})

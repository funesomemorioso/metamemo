from django.http import HttpResponse
from django.shortcuts import render
from metamemoapp.models import MetaMemo, MemoItem, MemoContext, MemoNews
from datetime import datetime, timedelta
# Create your views here.
def index(request):
    metamemo_list = MetaMemo.objects.all()
    data = {
        'social_list' : {},
    }
    return render(request, 'index.html', {'metamemo_list': metamemo_list, 'data': data})

def list(request, day=datetime.now().day, month=datetime.now().month, year=datetime.now().year):
    
    #ToDo: incluir data default 
    social_list =  request.POST.getlist('social_list')
    metamemo_selected_list =  request.POST.getlist('metamemo_selected_list')
    
    
    
    
    start_date  = request.POST["start_date"]
    end_date = request.POST["end_date"]

    date_start_obj = datetime.strptime(start_date, '%Y-%m-%d')
    date_end_obj = datetime.strptime(end_date, '%Y-%m-%d')

    day_s = date_start_obj.day
    month_s = date_start_obj.month
    year_s = date_start_obj.year

    day_e = date_end_obj.day
    month_e = date_end_obj.month
    year_e = date_end_obj.year
    
    
    

    memoitem_list = MemoItem.objects.filter(author__name__in=metamemo_selected_list, content_date__range=[start_date, end_date])[:20]
    memocontext_list = MemoContext.objects.filter(start_date__range=[start_date, end_date])
    memonews_list = MemoNews.objects.filter(content_date__range=[start_date, end_date])


    data = {
        'metamemo_selected_list' : metamemo_selected_list,
        'memocontext_list' : memocontext_list,
        'memonews_list' : memonews_list,
        'social_list' : social_list,
        'start_date' : start_date,
        'end_date' : end_date,
        'memoitem_list' : memoitem_list
    }
    

    return render(request, 'list.html', {'data':data})

def integra(request, item_id):
    
    memoitem = MemoItem.objects.get(pk=item_id)
    print(str(memoitem))
    data = {
        'social_list' : {},
        'memoitem': memoitem,   
        'item_id': item_id
    }
    return render(request, 'integra.html', {'data': data})

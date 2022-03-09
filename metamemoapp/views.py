from django.http import HttpResponse
from django.shortcuts import render
from metamemoapp.models import MetaMemo, MemoItem, MemoContext, MemoNews
from datetime import datetime
# Create your views here.
def index(request):
    metamemo_list = MetaMemo.objects.all()
    return render(request, 'index.html', {'metamemo_list': metamemo_list})

def list(request, day=datetime.now().day, month=datetime.now().month, year=datetime.now().year):
 
    social_list =  request.POST.getlist('social_list')
    metamemo_selected_list =  request.POST.getlist('metamemo_selected_list')
    
    memoitem_list = MemoItem.objects.filter(author__name__in=metamemo_selected_list)[:20]

    
    start_date  = request.POST["start_date"]
    end_date = request.POST["end_date"]
    data = {
        'metamemo_selected_list' : metamemo_selected_list,
        'social_list' : social_list,
        'start_date' : start_date,
        'end_date' : end_date,
        'memoitem_list' : memoitem_list
    }


    return render(request, 'list.html', {'data':data})
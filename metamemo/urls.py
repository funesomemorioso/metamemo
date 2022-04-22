"""metamemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from metamemoapp import views


urlpatterns = [
    path('', views.home, name='home'),
    path('content/<str:page>', views.content, name='content'),
    path('blog/', views.blog, name='blog'),
    path('blog/<str:post>', views.blog, name='blog'),
    path('search/', views.search, name='search'),
    path('search/<int:year>/<int:month>/<int:day>', views.search, name='search'),
    path('memoitem/<int:item_id>', views.memoitem, name='memoitem'),
    path('admin/', admin.site.urls),
    path('celery-progress/', include('celery_progress.urls')),
    path('__debug__', include('debug_toolbar.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

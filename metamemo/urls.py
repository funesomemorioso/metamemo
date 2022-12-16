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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog import views as blogviews
from metamemoapp import views

urlpatterns = [
    # "Static" pages
    path("content/<str:page>", views.content, name="content"),

    # Blog
    path("blog/", blogviews.blog_redir, name="blog"),
    path("blog/<str:post>", blogviews.blog_redir, name="blog"),

    # MemoItem-related
    path("", views.home, name="home"),
    path("lista/", views.lista, name="lista"),
    path("memoitems/download", views.memoitems_download, name="memoitems-download"),
    path("memoitem/<int:item_id>", views.memoitem, name="memoitem"),
    path("memoitem/<int:item_id>/get_media", views.get_media, name="get_media"),

    # MemoMedia-related
    path("transcricao/", views.media_list, name="media-list"),

    # NewsItem-related
    path("news/", views.news_list, name="news-list"),
    path("news/<int:item_id>", views.news_detail, name="news-detail"),

    # MemoContext-related
    path("contexts/", views.contexts, name="contexts"),

    # NewsCover-related
    path("newscovers/", views.news_covers, name="newscovers"),

    # Timeline-related
    path("timeline/", include("timeline.urls")),

    # Administrative
    path("admin/", admin.site.urls),
    path("celery-progress/", include("celery_progress.urls")),
    path("summernote/", include("django_summernote.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path("__debug__", include("debug_toolbar.urls"))]

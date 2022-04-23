from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator

# Create your views here.
def blog(request, post=None):
    if post:
        post = Post.objects.get(slug=post)
        return render(request, 'post.html', {'post': post })
    else:
        all_posts = Post.objects.all()
        posts = Paginator(all_posts, 50)
        return render(request, 'blog.html', {'posts' : posts.page(1)})

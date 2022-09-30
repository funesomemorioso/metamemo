from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .models import Post


# O blog não está mais hospedado no Django - agora temos um Medium
def blog_redir(request, post=None):
    return redirect("https://medium.com/@metamixblog")


def blog(request, post=None):
    if post:
        post = Post.objects.get(slug=post)
        return render(request, "post.html", {"post": post})
    else:
        all_posts = Post.objects.all()
        posts = Paginator(all_posts, 50)
        return render(request, "blog.html", {"posts": posts.page(1)})

from django.shortcuts import render
from django.views.decorators.http import require_GET

from posts.models import Post


@require_GET
def home(request):
    posts = Post.published.filter(pin=True)[:6]
    return render(request, "pages/home.html", {"post_list": posts})


@require_GET
def about(request):
    return render(request, "pages/about.html")


@require_GET
def robots(request):
    return render(request, "pages/robots.txt", content_type="text/plain")

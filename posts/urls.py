from django.urls import path

from .feeds import AtomPostFeed
from .views import PostListView, PostDetailView

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("feed/atom/", AtomPostFeed(), name="feed-atom"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
]

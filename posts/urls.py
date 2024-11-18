from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .feeds import AtomPostFeed
from .views import PostListView, PostDetailView, PostViewSet

app_name = "posts"

router = DefaultRouter()
router.register("v1", PostViewSet, basename="posts")

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("api/", include(router.urls)),
    path("feed/atom/", AtomPostFeed(), name="feed-atom"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
]

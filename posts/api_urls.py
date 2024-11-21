from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet

app_name = "posts"

router = DefaultRouter()
router.register("v1", PostViewSet, basename="posts")

urlpatterns = [
    path("api/", include(router.urls)),
]

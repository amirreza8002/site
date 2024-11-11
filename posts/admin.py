from django.contrib import admin

from .forms import PostForm
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ("title", "status")
    list_filter = ("status", "created_at", "published_at")
    search_fields = ("title", "body")
    ordering = ("-published_at", "status")
    prepopulated_fields = {"slug": ("title",)}

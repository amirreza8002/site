from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    model = Post
    fields = ("title", "slug", "body", "status", "tags", "pin", "image", "alt")

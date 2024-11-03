from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from .models import Post


class PostForm(ModelForm):
    model = Post
    fields = ("title", "slug", "body", "status", "tags", "pin")
    widgets = {"body": TinyMCE()}

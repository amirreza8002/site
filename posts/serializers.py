from rest_framework.serializers import ModelSerializer

from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Post


class PostSerializer(TaggitSerializer, ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ("title", "slug", "body", "image", "alt", "status", "tags", "pin")
        read_only_fields = ("created_at", "published_at", "updated_at")

import pytest
from django.test import TestCase

from posts.models import Post


class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        post1 = Post.objects.create(
            title="test",
            body="test body text",
            status="D",
        )
        post1.tags.set(["green", "blue"])

        post2 = Post.objects.create(
            title="pub",
            body="pub pub pub",
            status="P",
        )
        post2.tags.set(["red", "yellow"])

    def test_post1_exists(self):
        Post.objects.get(title="test")

    def test_post1_is_draft(self):
        post1 = Post.objects.get(title="test")
        post1.status = "D"
        with pytest.raises(Post.DoesNotExist):
            Post.published.get(title="test")

    def test_post1_tags(self):
        assert "green" in [tag.name for tag in Post.tags.all()]

    def test_post2_is_published(self):
        post2 = Post.objects.get(title="pub")
        post2.status = "P"
        Post.published.get(title="pub")

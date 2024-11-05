from django.test import TestCase
from django.urls import reverse

from posts.models import Post


class TestPostListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        post1 = Post.objects.create(
            title="Published Post",
            body="Published Body",
            status="P",
        )
        post1.tags.set(["green"])
        post2 = Post.objects.create(
            title="Draft post",
            body="Draft Body",
            status="D",
        )
        post2.tags.set(["red"])

    def test_list_view_available(self):
        response = self.client.get(reverse("posts:post-list"))
        assert response.status_code == 200

    def test_list_view_template(self):
        response = self.client.get(reverse("posts:post-list"))
        self.assertTemplateUsed(response, "posts/post_list.html")

    def test_list_view_shows_published_posts_not_draft(self):
        response = self.client.get(reverse("posts:post-list"))
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Draft Post")


class TestPostDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        post1 = Post.objects.create(
            title="Published Post",
            body="Published Body",
            status="P",
        )
        post1.tags.set(["green"])
        post2 = Post.objects.create(
            title="Draft post",
            body="Draft Body",
            status="D",
        )
        post2.tags.set(["red"])

    def test_detail_view_available(self):
        response = self.client.get(
            reverse("posts:post-detail", kwargs={"slug": "published-post"})
        )
        assert response.status_code == 200

    def test_detail_view_404_when_draft(self):
        response = self.client.get(
            reverse("posts:post-detail", kwargs={"slug": "draft-post"})
        )
        assert response.status_code == 404

    def test_detail_view_content(self):
        response = self.client.get(
            reverse("posts:post-detail", kwargs={"slug": "published-post"})
        )
        self.assertContains(response, "Published Post")

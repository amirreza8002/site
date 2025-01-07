from django.conf import settings
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class AtomPostFeed(Feed):
    title = "blog"
    link = "/en/blog/"
    subtitle = "Blog posts on my site"
    feed_type = Atom1Feed

    def items(self):
        return Post.published.filter(tags__name__in=("django",))[:100]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 40)

    def item_updateddate(self, item):
        return item.updated_at

    def feed_url(self):
        if settings.DEBUG:
            return "http://localhost:8000/en/blog/feed/atom"
        return "https://teapot.codes/en/blog/feed/atom"

    def author_name(self, obj):
        return "amirreza sohrabi far"

    def author_email(self, obj):
        return "amir.rsf1380@gmail.com"

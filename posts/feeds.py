from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class AtomPostFeed(Feed):
    title = "blog"
    link = "/blog/"
    subtitle = "Blog posts on my site"
    feed_type = Atom1Feed

    def items(self):
        return Post.published.all()[:100]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 40)

    def item_updateddate(self, item):
        return item.updated_at

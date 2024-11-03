from django.http import Http404
from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    queryset = Post.published.all()


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.published:
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

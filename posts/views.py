from django.http import Http404
from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context["paginator"]
        page = context["page_obj"]
        if page and paginator:
            prev_pages_number = page.number - 1
            next_pages_number = paginator.num_pages - page.number
            context["prev_pages_number"] = prev_pages_number
            context["next_pages_number"] = next_pages_number
        return context


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.status == "P":
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

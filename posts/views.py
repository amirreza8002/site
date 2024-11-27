# from django.core import serializers
from django.http import Http404
from django.views.generic import DetailView, ListView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer


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


# @require_GET
# def search_ajax(request):
#    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
#    if not is_ajax:
#        return JsonResponse({"fail": "most be an ajax request"}, status=404)
#    url_params = request.GET.get("q")

#    if url_params:
#        query = SearchQuery(url_params)
#        vector = SearchVector("title", "body")
#        search = Post.published.annotate(rank=SearchRank(vector, query)).order_by(
#            "-rank"
#        )[:5]
#        response = serializers.serialize(
#            "json", search, fields=["title", "body", "slug"]
#        )
#        return JsonResponse({"wrapper": response}, status=200)


class PostViewSet(ModelViewSet):
    lookup_field = "slug"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Post.published.all()
    serializer_class = PostSerializer

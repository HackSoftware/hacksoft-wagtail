from django.views import generic
from django.shortcuts import get_object_or_404

from .snippets import BlogPostSnippet


class BlogPostView(generic.TemplateView):
    template_name = 'website/blog_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post'] = get_object_or_404(BlogPostSnippet, slug=self.kwargs['slug'])
        return context


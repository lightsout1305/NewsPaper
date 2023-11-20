from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from news_project.models import Post


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['site'] = Site.objects.get_current().domain
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['content'] = Post.objects.filter(author_id=self.request.user.author.id).order_by('-register_date')
        return context

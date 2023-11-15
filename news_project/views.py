import pytz
import logging

from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.cache import cache
from django.template.loader import render_to_string

from .models import Post, Category, CategorySubscribers, Author, Comment
from .filters import PostFilter
from .forms import PostForm, CommentForm


from NewsPaper.settings import SERVER_EMAIL, TIME_ZONE


logger = logging.getLogger('django')


def index_test(request):
    logger.debug("Hello! --------DEBUG--------Enjoy:)")
    logger.info("Hello! --------INFO--------Enjoy:)")
    logger.warning("Hello! --------WARNING--------Enjoy:)")
    logger.error("Hello! --------ERROR--------Enjoy:)")
    logger.critical("Hello! --------CRITICAL--------Enjoy:)")
    return HttpResponse("<p> Сообщение для тестирования </p>")


def set_timezone(request):
    user_timezone = pytz.timezone(
        request.session.get('django_timezone') or TIME_ZONE
    )
    current_time = timezone.now().astimezone(user_timezone)
    context = {
        'current_time': current_time,
        'timezones': pytz.common_timezones,
    }
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('content_list')

    render(request, 'flatpages/default.html', context)


class NewsList(ListView):
    model = Post
    ordering = '-register_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5


class NewsSearch(ListView):
    model = Post
    ordering = '-register_date'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news_project.add_post', )

    def form_valid(self, form):
        news = form.save(commit=False)
        news.choice = 'NEWS'
        init_author = Author.objects.get(author_user=self.request.user)
        news.author = init_author
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    permission_required = ('news_project.add_post', )

    def form_valid(self, form):
        article = form.save(commit=False)
        article.choice = 'ARTL'
        init_author = Author.objects.get(author_user=self.request.user)
        article.author = init_author
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news_project.change_post', )

    def form_valid(self, form):
        news = form.save(commit=False)
        news.choice = 'NEWS'
        init_author = Author.objects.get(author_user=self.request.user)
        news.author = init_author
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('news_project.change_post',)

    def form_valid(self, form):
        article = form.save(commit=False)
        article.choice = 'ARTL'
        init_author = Author.objects.get(author_user=self.request.user)
        article.author = init_author
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('content_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('content_list')


class NewsDetail(FormView, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'detail.html'
    context_object_name = 'onenews'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news_detail-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news_detail-{self.kwargs["pk"]}', obj)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse("news_detail", kwargs={"pk": post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        context['comment'] = Comment
        return context


class CategoryDetail(PermissionRequiredMixin, ListView):
    model = Category
    context_object_name = 'category_detail'
    template_name = 'cat_sub.html'
    permission_required = ('news_project.view_category',)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['category_post'] = Post.objects.filter(postcategory=id)
        context['subscription_object'] = 'category_subscription'
        context['name'] = Category.objects.filter(id=id)
        is_subscribed = CategorySubscribers.objects.filter(linked_category=id, linked_user=user).exists()
        context['is_subscribed'] = is_subscribed
        return context


@login_required
def add_subscription(request, pk):
    user = request.user
    catgr = Category.objects.get(id=pk)
    is_subscribed = CategorySubscribers.objects.filter(linked_user_id=user.id, linked_category_id=catgr.id)

    if request.method == 'POST':
        if not is_subscribed:
            CategorySubscribers.objects.create(linked_user_id=user.id, linked_category_id=catgr.id)
            catgr_repr = f'{catgr}'
            email = user.email
            msg = EmailMultiAlternatives(
                subject=f'Subscription to {catgr_repr} category',
                body=f'Вы {user} успешно подписались на категорию {catgr_repr}',
                from_email=SERVER_EMAIL,
                to=[email, ],
            )
            html_content = render_to_string(
                'news_project/subscription_success.html',
                {
                    'user': user,
                    'category': catgr_repr,
                }
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

        elif not CategorySubscribers.objects.filter(linked_category_id=catgr.id):
            CategorySubscribers.objects.create(linked_user_id=user.id, linked_category_id=catgr.id)
            catgr_repr = f'{catgr}'
            email = user.email
            msg = EmailMultiAlternatives(
                subject=f'Subscription to {catgr_repr} category',
                body=f'Вы {user} успешно подписались на категорию {catgr_repr}',
                from_email=SERVER_EMAIL,
                to=[email, ],
            )
            html_content = render_to_string(
                'news_project/subscription_success.html',
                {
                    'user': user,
                    'category': catgr_repr,
                }
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    return redirect('/main/')


@login_required
def remove_subscription(request, pk):
    user = request.user
    catgr = Category.objects.get(id=pk)
    if CategorySubscribers.objects.filter(linked_user_id=user.id):
        CategorySubscribers.objects.filter(linked_category_id=catgr.id, linked_user_id=user.id).delete()
    return redirect('/main/')


def add_comment_like(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.like()
    return redirect(request.META.get('HTTP_REFERER'))


def add_comment_dislike(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.dislike()
    return redirect(request.META.get('HTTP_REFERER'))


def update_rating_up(request, pk):
    post = Post.objects.get(id=pk)
    post.like()
    return redirect(request.META.get('HTTP_REFERER'))


def update_rating_down(request, pk):
    post = Post.objects.get(id=pk)
    post.dislike()
    return redirect(request.META.get('HTTP_REFERER'))

# Create your views here.

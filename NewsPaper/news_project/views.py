from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'register_date'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'onenews'
    pk_url_kwarg = 'id'

# Create your views here.

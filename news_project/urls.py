from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, \
    ArticleDelete, CategoryDetail, add_subscription, remove_subscription, index_test, add_comment_like, \
    add_comment_dislike, update_rating_up, update_rating_down
from django.views.decorators.cache import cache_page

import logging

logger_dr = logging.getLogger('django.request')
logger_cn = logging.getLogger('django')

# logger_dr.error("Hello! I'm error in your app. Enjoy:)")
# logger_cn.error("Hello! I'm error in your app. Enjoy:)")
# ----------КОНЕЦ тестирования логирования-----------

urlpatterns = [
    path('test/', index_test, name='index_test'),
    path('', NewsList.as_view(), name='content_list'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('search/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
    path('categories/', CategoryDetail.as_view(template_name='cat_sub.html'), name='category'),
    path('categories/subscribe/category/<int:pk>', add_subscription, name='subscribe_to_category'),
    path('categories/unsubscribe/category/<int:pk>', remove_subscription, name='unsubscribe_to_category'),
    path('plusratingcomment/<int:pk>/', add_comment_like, name='add_comment_like'),
    path('minusratingcomment/<int:pk>/', add_comment_dislike, name='add_comment_dislike'),
    path('pluscontent/<int:pk>/', update_rating_up, name='add_content_like'),
    path('minuscontent/<int:pk>/', update_rating_down, name='add_content_dislike'),
]

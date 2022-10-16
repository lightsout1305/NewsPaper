from rest_framework.routers import SimpleRouter

from .views import NewsAPIViewSet, ArticleAPIViewSet


router = SimpleRouter()

router.register('news', NewsAPIViewSet, basename='news')
router.register('articles', ArticleAPIViewSet, basename='articles')

urlpatterns = router.urls



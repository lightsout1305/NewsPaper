from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from news_project.models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly


class NewsAPIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.filter(choice='NEWS')
    serializer_class = PostSerializer


class ArticleAPIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.filter(choice='ARTL')
    serializer_class = PostSerializer

# Create your views here.

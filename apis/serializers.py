from rest_framework import serializers

from news_project.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'author',
            'title',
            'content',
            'categories',
            'register_date',
        )
        model = Post

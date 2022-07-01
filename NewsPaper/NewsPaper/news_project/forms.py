from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=150)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
            'categories',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title == content:
            raise ValidationError(
                'Название и содержимое статьи (новости) не должны совпадать'
            )
        return cleaned_data



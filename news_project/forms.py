from django import forms
from django.utils.translation import gettext as _
from .models import Post, Comment
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = _("Title")
        self.fields['title'].widget.attrs.update({'style': 'font-size: 30px'})
        self.fields['content'].label = _("Content")
        self.fields['content'].widget.attrs.update({'style': 'font-size: 20px'})
        self.fields['categories'].label = _("Categories")
        self.fields['image'].label = _("Image")

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'categories',
            'image'
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


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(widget=forms.Textarea, label="")

    class Meta:
        model = Comment
        fields = ('comment_text',)

from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, CharFilter
from .models import Post, Category
from django.forms import DateInput


class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr='icontains',
        label='Type title'
    )

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects,
        label='News Categories',
        conjoined=True
    )

    register_date = DateFilter(
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date'
            },
        ),
        label='Choose date'
    )

    class Meta:
        model = Post
        fields = {}

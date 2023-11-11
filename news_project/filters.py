from django.utils.translation import gettext as _
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, CharFilter
from .models import Post, Category
from django.forms import DateInput


class PostFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['title'].label = _("Type title")
        self.filters['category'].label = _("News categories")
        self.filters['register_date'].label = _("Select date")

    title = CharFilter(
        lookup_expr='icontains'
    )

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects,
        conjoined=True
    )

    register_date = DateFilter(
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date'
            },
        ),
        label='Choose date',
    )

    class Meta:
        model = Post
        fields = {}

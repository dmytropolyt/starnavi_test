from django_filters import rest_framework as filters

from .models import Post


class PostFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['created_at']

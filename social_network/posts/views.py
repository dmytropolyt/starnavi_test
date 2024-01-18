from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import (
    extend_schema_view, extend_schema,
)

from .models import Post
from .serializers import PostSerializer
from .mixins import LikeModelMixin
from .filters import PostFilter


@extend_schema_view(
    list=extend_schema(
        description='List all posts'
    ),
    create=extend_schema(
        description='Create a new post'
    ),
    retrieve=extend_schema(
        description='Retrieve a post'
    ),
    update=extend_schema(
        description='Update whole post'
    ),
    partial_update=extend_schema(
        description='Update part of post'
    ),
    destroy=extend_schema(
        description='Delete a post'
    )
)
class PostViewSet(LikeModelMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

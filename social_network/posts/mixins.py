from rest_framework.response import Response
from rest_framework.decorators import action


class LikeModelMixin:
    """
    Like and unlike model instance.
    """
    @action(detail=True, methods=['post'])
    def like(self, request, *args, **kwargs):
        object = self.get_object()
        object.likes.add(request.user)

        return Response({'status': 'liked'})

    @action(detail=True, methods=['delete'])
    def unlike(self, request, *args, **kwargs):
        object = self.get_object()
        object.likes.clear()

        return Response({'status': 'unliked'})

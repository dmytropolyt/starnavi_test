from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import (
    extend_schema_view, extend_schema,
)

from .serializers import (
    RegisterUserSerializer,
    CustomTokenObtainPairSerializer,
    UserActivitySerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny, )
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        description='Register a new user.'
    ),
)
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterUserSerializer


@extend_schema_view(
    get=extend_schema(
        description='Get last user activity'
    )
)
class UserActivityView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer

    def get_object(self):
        if self.kwargs.get('pk') == 'me':
            self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

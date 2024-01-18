from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterUserView,
    CustomTokenObtainPairView,
    UserActivityView
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user-register'),

    path(
        'token/', CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path(
        'users/me', UserActivityView.as_view(),
        name='user-activity', kwargs={'pk': 'me'}
    )
]

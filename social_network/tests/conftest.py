import pytest
from pytest_factoryboy import register

from django.urls import reverse

from . import factories

register(factories.UserFactory)
register(factories.PostFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_auth(api_client, user_factory):
    api_client.post(reverse('user-register'), {
        'username': 'Test', 'password': 'testpass12',
        'password2': 'testpass12'
    })
    url = reverse('token_obtain_pair')

    jwt = api_client.post(url, {
        'username': 'Test',
        'password': 'testpass12'
    })

    print(jwt.json())
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt.data['access']}")

    return api_client

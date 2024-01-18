import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestUsersAPI:
    test_data = {
        'username': 'Test',
        'password': 'testpass12',
        'password2': 'testpass12'
    }

    def test_user_registration(self, api_client, django_user_model):
        url = reverse('user-register')

        response = api_client.post(
            url,
            {'username': self.test_data.get('username'),
             'password': self.test_data.get('password'),
             'password2': self.test_data.get('password2')}
        )

        user = django_user_model.objects.get(
            username=self.test_data.get('username')
        )

        assert response.status_code == 201
        assert user.username == self.test_data['username']

    def test_user_obtain_token(self, api_client_auth):
        url = reverse('token_obtain_pair')

        response = api_client_auth.post(url, {
            'username': self.test_data.get('username'),
            'password': self.test_data.get('password')
        })

        response_content = response.json()

        jwt_token_names = ('refresh', 'access')
        for key, value in response_content.items():
            assert key in jwt_token_names
            assert bool(value) is True

    def test_user_activity(self, api_client_auth):
        url = reverse('user-activity')

        response = api_client_auth.get(url)

        assert response.status_code == 200

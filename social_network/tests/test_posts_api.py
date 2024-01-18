import pytest

import datetime

from django.urls import reverse

from freezegun import freeze_time

from posts.models import Post


@pytest.mark.django_db
class TestPostsAPI:
    model = Post
    test_data = {
        'title': 'test',
        'body': 'testbody'
    }

    def test_post_list(self, api_client_auth, post_factory):
        post_factory.create_batch(10)
        url = reverse('post-list')

        response = api_client_auth.get(url)

        assert len(response.json()) == Post.objects.count()

    def test_post_create(self, api_client, user_factory):
        user = user_factory.create()
        api_client.force_authenticate(user=user)

        response = api_client.post(reverse('post-list'), {
            'title': self.test_data.get('title'),
            'body': self.test_data.get('body')
        })

        post = Post.objects.get(author=user)

        assert response.status_code == 201
        assert post.title == self.test_data.get('title')
        assert post.body == self.test_data.get('body')

    def test_post_retrieve(self, api_client_auth, post_factory):
        post = post_factory.create()
        url = reverse('post-detail', kwargs={'pk': post.pk})

        response = api_client_auth.get(url)
        content = response.json()
        print(content)
        assert response.status_code == 200
        assert content['title'] == post.title
        assert content['author'] == post.author.username
        assert content['body'] == post.body

    def test_post_update(self, api_client_auth, post_factory):
        post = post_factory.create()
        url = reverse('post-detail', kwargs={'pk': post.pk})

        response = api_client_auth.put(url, {
            'title': self.test_data.get('title'),
            'body': self.test_data.get('body')
        })

        content = response.json()

        assert response.status_code == 200
        assert content['title'] == self.test_data.get('title')
        assert content['body'] == self.test_data.get('body')

    def test_post_partial_update(self, api_client_auth, post_factory):
        post = post_factory.create()
        url = reverse('post-detail', kwargs={'pk': post.pk})

        response = api_client_auth.patch(url, {
            'title': self.test_data.get('title')
        })

        assert response.status_code == 200
        assert response.json()['title'] == self.test_data.get('title')

    def test_post_delete(self, api_client_auth, post_factory):
        post = post_factory.create()
        url = reverse('post-detail', kwargs={'pk': post.pk})

        response = api_client_auth.delete(url)
        response_get = api_client_auth.get(url)

        assert response.status_code == 204
        assert response_get.status_code == 404

    def test_post_like(self, api_client_auth, post_factory):
        post = post_factory.create()
        url = reverse('post-like', kwargs={'pk': post.pk})

        response = api_client_auth.post(url)
        content = response.json()

        assert response.status_code == 200
        assert content == {'status': 'liked'}

    def test_post_unlike(self, api_client_auth, post_factory):
        post = post_factory.create()
        api_client_auth.post(reverse('post-like', kwargs={'pk': post.pk}))

        url = reverse('post-unlike', kwargs={'pk': post.pk})

        response = api_client_auth.delete(url, follow=True)
        content = response.json()
        like = post.likes.first()

        assert response.status_code == 200
        assert content == {'status': 'unliked'}
        assert like is None

    def test_post_filter_created_at_after(self, api_client_auth, post_factory):
        with freeze_time('2024-03-15'):
            post_factory.create_batch(5, created_at=datetime.datetime.now())

        with freeze_time('2024-01-15'):
            post_factory.create_batch(5, created_at=datetime.datetime.now())

        response = api_client_auth.get(
            reverse('post-list'), {'created_at_after': '2024-02-15'}
        )
        content = response.json()

        assert response.status_code == 200
        assert len(content) == 5
        for post in content:
            assert '2024-03-15' in post['created_at']

    def test_post_filter_created_at_before(self, api_client_auth, post_factory):
        with freeze_time('2024-03-15'):
            post_factory.create_batch(5, created_at=datetime.datetime.now())

        with freeze_time('2024-01-15'):
            post_factory.create_batch(5, created_at=datetime.datetime.now())

        response = api_client_auth.get(
            reverse('post-list'), {'created_at_before': '2024-02-15'}
        )
        content = response.json()

        assert response.status_code == 200
        assert len(content) == 5
        for post in content:
            assert '2024-01-15' in post['created_at']

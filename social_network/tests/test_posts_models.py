import pytest

from django.db.utils import IntegrityError

from posts.models import Post


@pytest.mark.django_db
class TestPostModel:
    """Tests for Post model."""
    model = Post
    test_data = {
        'title': 'test title',
        'body': 'test body'
    }

    def test_create_post_with_author(self, user_factory):
        author = user_factory.create()
        self.model.objects.create(
            title=self.test_data.get('title'),
            author=author,
            body=self.test_data.get('body')
        )

        post = self.model.objects.get(author=author)

        assert post.author == author
        assert post.title == self.test_data.get('title')
        assert post.body == self.test_data.get('body')

    def test_create_post_without_author(self):
        with pytest.raises(IntegrityError):
            self.model.objects.create(
                title=self.test_data.get('title'),
                body=self.test_data.get('body')
            )

    def test_post_likes(self, post_factory, user_factory):
        post = post_factory.create()
        user = user_factory.create()
        post.likes.add(user)

        likes = post.likes.all()

        assert len(likes) == 1

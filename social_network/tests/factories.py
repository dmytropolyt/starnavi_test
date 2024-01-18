import factory

from django.contrib.auth import get_user_model

from posts.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.sequence(lambda n: f'Test{n}')
    password = 'testpass12'


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.sequence(lambda n: f'Title #{n}')
    author = factory.SubFactory(UserFactory)
    body = factory.sequence(lambda n: f'Body {n}')
    created_at = factory.Faker('date_time_this_decade', tzinfo=None)

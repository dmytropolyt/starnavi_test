import random
from typing import Union

import requests

from faker import Faker

from config import settings

fake = Faker()


class Bot:
    @staticmethod
    def signup_users() -> list[dict[str, str]]:
        users_data = [
            {
                'username': fake.user_name(),
                'password': (password := fake.password()),
                'password2': password
            } for _ in range(settings.NUMBER_OF_USERS)
        ]

        for user in users_data:
            requests.post(
                settings.REGISTER_URL,
                user
            )

        return users_data

    @staticmethod
    def users_login(
            users_data: list[dict[str, Union[str, dict]]]
    ) -> list[dict[str, Union[str, dict]]]:
        for user in users_data:
            response = requests.post(
                settings.TOKEN_OBTAIN_URL,
                {'username': user.get('username'),
                 'password': user.get('password')}
            )

            headers = {'Authorization': f'Bearer {response.json()["access"]}'}
            user['header_auth'] = headers

        return users_data

    @staticmethod
    def post_request_random_times(
            stop_number: int, url: str,
            headers: dict[str, str],
            data: dict[str, str] | None = None
    ) -> None:
        for i in range(random.randrange(stop_number)):
            requests.post(url, headers=headers, data=data)

    def user_create_posts(self) -> None:
        new_users = self.signup_users()
        users_data = self.users_login(new_users)

        for user in users_data:
            self.post_request_random_times(
                settings.MAX_POSTS_PER_USER,
                settings.CREATE_POST,
                user.get('header_auth'),
                data={'title': fake.sentence(),
                      'body': fake.paragraph()}
            )

    def like_random_posts(self) -> None:
        new_users = self.signup_users()
        users_data = self.users_login(new_users)

        first_user = users_data[0]
        all_posts_count = len(requests.get(
            settings.LIST_POSTS,
            headers=first_user.get('header_auth')
        ).json())

        for user in users_data:
            self.post_request_random_times(
                settings.MAX_LIKES_PER_USER,
                settings.LIKE_POST.format(
                    post_id=random.randrange(1, all_posts_count + 1)
                ),
                user.get('header_auth')
            )


if __name__ == '__main__':
    bot = Bot()
    bot.user_create_posts()
    bot.like_random_posts()

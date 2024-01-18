from dataclasses import dataclass


@dataclass
class Settings:
    API_MAIN_URL: str = 'http://127.0.0.1:8000/api/v1/'
    REGISTER_URL: str = f'{API_MAIN_URL}register/'
    TOKEN_OBTAIN_URL: str = f'{API_MAIN_URL}token/'
    LIST_POSTS: str = f'{API_MAIN_URL}post/'
    CREATE_POST: str = f'{API_MAIN_URL}post/'
    LIKE_POST: str = f'{API_MAIN_URL}post/{{post_id}}/like/'
    NUMBER_OF_USERS: int = 3
    MAX_POSTS_PER_USER: int = 5
    MAX_LIKES_PER_USER: int = 5


settings = Settings()

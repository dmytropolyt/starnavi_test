from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    body = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_like')

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title

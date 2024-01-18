from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            'author', 'title', 'body',
            'created_at', 'likes_count'
        ]
        read_only_fields = ['created_at', 'likes_count']

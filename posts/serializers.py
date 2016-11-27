from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'short_description', 'categories', 'image_url')


class PostListSerializer(PostSerializer):

    class Meta(PostSerializer.Meta):
        fields = ("id", "title", "image_url", "short_description", "publication_date")

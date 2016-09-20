from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post


class PostListSerializer(PostSerializer):

    class Meta(PostSerializer.Meta):
        fields = ("title", "image_url", "short_description", "publication_date")

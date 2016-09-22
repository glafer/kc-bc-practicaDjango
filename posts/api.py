from django.utils.datetime_safe import datetime
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from posts.serializers import PostSerializer, PostListSerializer
from practica.permissions import UserPermissionOnPosts


class PostViewSet(ModelViewSet):

    serializer_class = Post
    permission_classes = (UserPermissionOnPosts,)
    search_fields = ('title', 'short_description', 'body')
    order_fields = ('title', 'publication_date')
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)

    def get_queryset(self):
        posts = Post.objects.all().select_related("owner")
        if posts[0].owner != self.request.user or not self.request.user.is_staff:
            posts = posts.filter(publication_date__lt=datetime.now())
        return posts

    def get_serializer_class(self):
        return PostSerializer if self.action != 'list' else PostListSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

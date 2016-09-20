from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blogs.views import BlogQueryset
from posts.serializers import PostSerializer, PostListSerializer


class PostListAPI(ListCreateAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_fields = ('title', 'body',)
    order_fields = ('title', 'publication_date',)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)

    def get_queryset(self):
        username = self.kwargs['username']
        return BlogQueryset.get_posts_from_blog_by_user(User.objects.filter(username=username.replace('@', '')),
                                                        self.request.user)

    def get_serializer_class(self):
        return PostSerializer if self.request.method == 'POST' else PostListSerializer


class PostDetailAPI(RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        username = self.kwargs['username']
        pk = self.kwargs['pk']
        possibles_posts = BlogQueryset.get_posts_from_blog_by_user(User.objects.filter(username=username.replace('@', '')),
                                                        self.request.user)
        return possibles_posts.filter(pk=pk)

    def perform_update(self, serializer):
        username = self.kwargs['username']
        owner = User.objects.filter(username=username.replace('@', ''))
        if owner[0] == self.request.user or self.request.user.is_staff:
            return serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("Don't have necessary permisions")

    def perform_destroy(self, instance):
        username = self.kwargs['username']
        owner = User.objects.filter(username=username.replace('@', ''))
        if owner[0] == self.request.user or self.request.user.is_staff:
            return instance.delete()
        else:
            raise PermissionDenied("Don't have necessary permisions")

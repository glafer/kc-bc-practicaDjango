from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from blogs.serializers import BlogSerializer, BlogListSerializer
from practica.permissions import UserPermissionOnBlogs


class BlogViewSet(ModelViewSet):

    serializer_class = User
    permission_classes = [UserPermissionOnBlogs, ]
    search_fields = ('first_name',)
    order_fields = ('first_name',)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return BlogSerializer if self.action != 'list' else BlogListSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        return serializer.save()

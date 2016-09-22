from django.conf.urls import url, include
from rest_framework import views

from rest_framework.routers import DefaultRouter

from posts.api import PostViewSet
from posts.views import HomeView, PostView, PostCreationView

router = DefaultRouter()
router.register(r'api/1.0/posts', PostViewSet, base_name="api_blogs")

urlpatterns = [
    # Web URLS
    url(r'^blogs/(?P<username>@\w+)/(?P<pk>[0-9]+)$', PostView.as_view(), name='post_details'),
    url(r'^blogs/new-post', PostCreationView.as_view(), name="post_creation"),
    url(r'^$', HomeView.as_view(), name='posts_home'),

    # API URLS
    url(r'', include(router.urls))
]
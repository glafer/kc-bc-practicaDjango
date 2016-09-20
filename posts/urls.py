from django.conf.urls import url

#from photos.api import PhotoListAPI
from posts.api import PostListAPI, PostDetailAPI
from posts.views import HomeView, PostView, PostCreationView

urlpatterns = [
    # Web URLS
    url(r'^$', HomeView.as_view(), name='posts_home'),
    url(r'^blogs/(?P<username>@\w+)/(?P<pk>[0-9]+)$', PostView.as_view(), name='post_details'),
    url(r'^blogs/new-post', PostCreationView.as_view(), name="post_creation"),

    # API URLS
    url(r'^api/1.0/blogs/(?P<username>@\w+)$', PostListAPI.as_view(), name='api_posts_list'),
    url(r'^api/1.0/blogs/(?P<username>@\w+)/(?P<pk>[0-9]+)$', PostDetailAPI.as_view(), name='api_posts_detail'),
    url(r'^api/1.0/blogs/new-post/$', PostListAPI.as_view(), name='api_posts_detail'),
]
from django.conf.urls import url

#from photos.api import PhotoListAPI
from posts.views import HomeView, PostView, PostCreationView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='posts_home'),
    url(r'^blogs/(?P<username>@\w+)/(?P<pk>[0-9]+)$', PostView.as_view(), name='post_details'),
    url(r'^blogs/new-post', PostCreationView.as_view(), name="post_creation")
]
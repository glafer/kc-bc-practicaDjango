from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from blogs.views import ListView, LoginView, LogoutView, SignUpView, BlogView
from blogs.api import BlogViewSet

router = DefaultRouter()
router.register('api/1.0/blogs', BlogViewSet, base_name="api_blogs")

urlpatterns = [
    # Web URLS
    url(r'^blogs/$', ListView.as_view(), name='blogs_list'),
    url(r'^login/$', LoginView.as_view(), name='users_login'),
    url(r'^logout/$', LogoutView.as_view(), name='users_logout'),
    url(r'^signup/$', SignUpView.as_view(), name='users_signup'),
    url(r'^blogs/(?P<username>@\w+)$', BlogView.as_view(), name='blog_view'),

    # API URLS
    url(r'', include(router.urls))
]

from django.conf.urls import url


from blogs.views import ListView, LoginView, LogoutView, SignUpView, BlogView
from blogs.api import BlogDetailAPI, BlogListAPI

urlpatterns = [
    # Web URLS
    url(r'^blogs/$', ListView.as_view(), name='blogs_list'),
    url(r'^login/$', LoginView.as_view(), name='users_login'),
    url(r'^logout/$', LogoutView.as_view(), name='users_logout'),
    url(r'^signup/$', SignUpView.as_view(), name='users_signup'),
    url(r'^blogs/(?P<username>@\w+)$', BlogView.as_view(), name='blog_view'),

    # API URLS
    url(r'^api/1.0/blogs/$', BlogListAPI.as_view(), name='api_blogs_list'),
    url(r'^api/1.0/blogs/(?P<pk>[0-9]+)$', BlogDetailAPI.as_view(), name='api_blogs_detail'),
]

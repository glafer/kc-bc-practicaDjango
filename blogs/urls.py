from django.conf.urls import url


from blogs.views import ListView, LoginView, LogoutView, SignUpView

urlpatterns = [
    url(r'^blogs/$', ListView.as_view(), name='blogs_list'),
    url(r'^login/$', LoginView.as_view(), name='users_login'),
    url(r'^logout/$', LogoutView.as_view(), name='users_logout'),
    url(r'^signup/$', SignUpView.as_view(), name='users_signup'),
]
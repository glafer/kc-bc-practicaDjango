from django.conf.urls import url

#from photos.api import PhotoListAPI
from posts.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='posts_home'),

]
from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

from categories.models import Category


class Post(models.Model):

    title = models.CharField(max_length=250)
    short_description = models.CharField(max_length=500)
    body = models.TextField(null=True, blank=True)
    image_url = models.URLField()
    publication_date = models.DateTimeField(default=datetime.now, blank=True)
    categories = models.ManyToManyField(Category)
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

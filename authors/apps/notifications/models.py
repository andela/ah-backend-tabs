from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from django.utils import timezone


class Notifications(models.Model):
    user_to_notify = models.ForeignKey(User,related_name="user_to_notify", on_delete = models.CASCADE, blank = True)
    author = models.ForeignKey(User,related_name="author", on_delete = models.CASCADE, blank = True)
    article = models.ForeignKey(Article, on_delete = models.CASCADE, blank = True)
    read_or_not_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-created',)








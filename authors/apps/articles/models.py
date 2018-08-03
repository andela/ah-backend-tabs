from django.db import models
from authors.apps.authentication.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
import uuid


class Article(models.Model):
    title = models.CharField(max_length = 500)
    description = models.TextField()
    slug = models.SlugField(max_length = 255)
    body = models.TextField()
    created_at = models.DateTimeField(editable = False)
    updated_at  = models.DateTimeField(blank = True, null = True)
    author = models.ForeignKey(User, related_name = "user_articles", on_delete = models.CASCADE)
    favorited = models.BooleanField(default = False)
    favoritesCount = models.IntegerField(default = 0)
    tags = TaggableManager(blank = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title).replace("_","-")
            article_class = self.__class__
            qs_exists = article_class.objects.filter(slug=self.slug)
            if qs_exists:
                self.slug = self.slug + "-" + str(uuid.uuid4()).replace("_","-")
            self.created_at = timezone.now()
            return super(Article, self).save(*args, **kwargs)
        self.updated_at = timezone.now()
        return super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name = "article_images", on_delete = models.CASCADE)
    image = models.ImageField()

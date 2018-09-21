from django.db import models
from authors.apps.authentication.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
import uuid
from statistics import mean


class Article(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    slug = models.SlugField(max_length=255, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(
        User, related_name="user_articles", on_delete=models.CASCADE)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    rating = models.PositiveIntegerField(blank=True, editable=False, null=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    likesCount = models.IntegerField(default=0)
    dislikes = models.ManyToManyField(
        User, related_name="dislikes", blank=True)
    dislikesCount = models.IntegerField(default=0)
    favorites = models.ManyToManyField(
        User, related_name="favorites", blank=True)
    image = models.TextField(null=True, blank=True)
    viewsCount = models.IntegerField(default=0)
    views = models.ManyToManyField(User, related_name="views", blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title).replace("_", "-")
            article_class = self.__class__
            qs_exists = article_class.objects.filter(slug=self.slug)
            if qs_exists:
                self.slug = self.slug + "-" + \
                    str(uuid.uuid4()).replace("_", "-")
            self.created_at = timezone.now()
            return super(Article, self).save(*args, **kwargs)
        self.updated_at = timezone.now()
        return super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Rating(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.ForeignKey(
        User, related_name="user_article_rating", on_delete=models.CASCADE, blank=True)
    article = models.ForeignKey(
        Article, related_name="article_ratings", on_delete=models.CASCADE, blank=True)
    amount = models.PositiveIntegerField(choices=RATING_CHOICES)

    class Meta:
        ordering = ('-amount', )

    def av_rating(self, qs_set, new_rating=None):
        if new_rating:
            new_qs_set_ratings = [rating.amount for rating in qs_set]
            new_qs_set_ratings.append(new_rating)
            return round(mean(new_qs_set_ratings))
        qs_set_ratings = [rating.amount for rating in qs_set]
        return round(mean(qs_set_ratings))

    def save(self, *args, **kwargs):
        rating_class = self.__class__
        qs_exists = rating_class.objects.filter(
            article=self.article).filter(user=self.user)
        if len(qs_exists) == 0:
            existing_ratings = self.article.article_ratings.all()
            if existing_ratings:
                Article.objects.filter(pk=self.article.id).update(
                    rating=self.av_rating(existing_ratings, self.amount))
                return super(Rating, self).save(*args, **kwargs)
            article = Article.objects.get(pk=self.article.id)
            article.rating = self.amount
            article.save()
            return super(Rating, self).save(*args, **kwargs)
        qs_exists.update(amount=self.amount)
        ratings = self.article.article_ratings.all()
        Article.objects.filter(pk=self.article.id).update(
            rating=self.av_rating(ratings))
        return 

    def __str__(self):
        return 'Rating of {} on {} by user {}'.format(self.amount, self.article, self.user)


class Comment(models.Model):
    author = models.ForeignKey(
        User, related_name="comment_author", on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name="user_comments", on_delete=models.CASCADE, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(editable=False, auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.body

class TextComment(models.Model):
    author = models.ForeignKey(User, related_name="text_comment_author", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="user_text_comments", on_delete=models.CASCADE, blank=True)
    selected = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(editable=False, auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'selected text: {} and comment {}'.format(self.selected,self.body) 

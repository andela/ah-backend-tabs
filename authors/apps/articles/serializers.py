from rest_framework import serializers
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Rating, Comment

from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)
from django.utils import timezone


class CreateArticleSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField(required=False)
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        user = {
            "username": obj.author.username,
            "email": obj.author.email,
            "bio": obj.author.bio,
            "image":obj.author.image
        }
        return user

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'created_at', 'updated_at',
                  'author', 'favorited', 'favoritesCount', 'likesCount', 'dislikesCount', 'tags','image','rating']


class RateArticleSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = {
            "username": obj.user.username,
            "email": obj.user.email
        }
        return user

    def get_article(self, obj):
        article = Article.objects.filter(slug = obj.article.slug)
        rating = article[0].rating
        article = {
            "title": obj.article.title,
            "slug": obj.article.slug,
            "averageRating": rating
        }
        return article

    class Meta:
        model = Rating
        fields = ['amount', 'article', 'user']


class CreateCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = {
            "username": obj.author.username,
            "email": obj.author.email,
            "bio": obj.author.bio,
            "image": obj.author.image
        }
        return author

    def get_article(self, obj):
        article = {
            "title": obj.article.title,
        }
        return article

    class Meta:
        model = Comment
        fields = '__all__'


class UpdateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'description', 'body',]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.updated_at = timezone.now
        instance.save()
        return instance
        

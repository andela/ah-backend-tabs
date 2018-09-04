from rest_framework import serializers
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Rating, Comment

from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)
from django.utils import timezone
from .models import ArticleImage


class CreateArticleSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField(required=False)
    author = serializers.SerializerMethodField()
    article_images = serializers.SerializerMethodField()

    def get_author(self, obj):
        user = {
            "username": obj.author.username,
            "email": obj.author.email,
            "bio": obj.author.bio
        }
        return user

    def get_article_images(self, obj):
        image_array = []
        images = obj.article_images.all()

        for image in images:
            image_array.append(image.image.url)

        return image_array

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'created_at', 'updated_at',
                  'author', 'favorited', 'favoritesCount', 'likesCount', 'dislikesCount', 'tags','article_images']


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
        return obj.article.title

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
        

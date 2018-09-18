from rest_framework import serializers
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Rating
from authors.apps.notifications.models import Notifications

from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)
from django.utils import timezone

class RetrieveNotificationSerializer(serializers.ModelSerializer):
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
            "slug": obj.article.slug,
        }
        return article

    class Meta:
        model = Notifications
        fields = '__all__'



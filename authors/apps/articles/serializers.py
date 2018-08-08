from rest_framework import serializers
from authors.apps.authentication.models import User
from .models import Article, Rating

from taggit_serializer.serializers import (TagListSerializerField,TaggitSerializer)


class CreateArticleSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField(required = False)
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        user = {
            "username": obj.author.username,
            "email": obj.author.email
        }
        return user

    class Meta:
        model = Article
        fields = ['title','description','body','created_at','updated_at','author','favorited','favoritesCount','tags']

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
        fields = ['amount','article','user']

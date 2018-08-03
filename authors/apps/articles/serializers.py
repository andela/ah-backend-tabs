from rest_framework import serializers
from authors.apps.authentication.models import User 
from .models import Article

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
        

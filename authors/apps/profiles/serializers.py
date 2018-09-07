from django.contrib.auth import authenticate
from authors.apps.authentication.models import User
from rest_framework import serializers
from django.utils import timezone


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image',instance.image)
        instance.updated_at = timezone.now
        instance.save()
        return instance
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def retrieve(self,instance):
        return instance
        


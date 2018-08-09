from rest_framework import serializers
from authors.apps.authentication.models import User
from .models import Connect

class FollowUserSerializer(serializers.ModelSerializer):

    user_from = serializers.SerializerMethodField()
    user_to = serializers.SerializerMethodField()

    def get_user_from(self, obj):
        return obj.user_from.username

    def get_user_to(self, obj):
        return obj.user_to.username
  
    class Meta:
        model = Connect
        fields = ['user_from','user_to','created']

class Follow_Follower_ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','email']


        

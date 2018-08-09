from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from .serializers import FollowUserSerializer, Follow_Follower_ListSerializer
from rest_framework.permissions import IsAuthenticated
from authors.apps.authentication.models import User
from authors.apps.authentication.backends import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Connect
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .renderers import FollowerJSONRenderer, FollowingJSONRenderer

class FollowAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "username"
    
    def post(self, *args, **kwargs):
        username = self.kwargs.get(self.look_url_kwarg)
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        user_to = get_object_or_404(User, username = username)
        connection_exists = Connect.objects.filter(user_from = user_data[0]).filter(user_to = user_to)
        if connection_exists:
            return Response({"message":"You already followed this user!"}, status=status.HTTP_403_FORBIDDEN)
        message = "You are following {}!".format(user_to.username)
        Connect.objects.create(user_from = user_data[0], user_to = user_to)
        return Response({"message":message}, status=status.HTTP_200_OK)
        

class UnfollowAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "username"

    def delete(self, *args, **kwargs):
        username = self.kwargs.get(self.look_url_kwarg)
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        user = get_object_or_404(User, username = username)
        connection_exists = Connect.objects.filter(user_from = user_data[0]).filter(user_to = user)
        if not connection_exists:
            return Response({"message":"You are not following this user!"}, status=status.HTTP_403_FORBIDDEN)
        connection_exists.delete()
        message = "You unfollowed {}!".format(user.username)
        return Response({"message":message}, status=status.HTTP_200_OK)

class ListFollowers(ListAPIView):
        permission_classes = (IsAuthenticated, )
        serializer_class = Follow_Follower_ListSerializer
        pagination_class = PageNumberPagination
        renderer_classes = (FollowerJSONRenderer,)

        def get_queryset(self):
            jwt = JWTAuthentication()
            user_data = jwt.authenticate(self.request)
            followers = user_data[0].followers.all()
            return followers


class ListFollowing(ListAPIView):
        permission_classes = (IsAuthenticated, )
        serializer_class = Follow_Follower_ListSerializer
        pagination_class = PageNumberPagination
        renderer_classes = (FollowingJSONRenderer,)

        def get_queryset(self):
            jwt = JWTAuthentication()
            user_data = jwt.authenticate(self.request)
            following = user_data[0].following.all()
            return following


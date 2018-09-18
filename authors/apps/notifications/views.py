from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import RetrieveNotificationSerializer
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Comment
from rest_framework.permissions import IsAuthenticated, AllowAny
from authors.apps.authentication.backends import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from ..notifications.models import Notifications


from authors.apps.authentication.backends import JWTAuthentication

from rest_framework.response import Response
from rest_framework import status
import json


class RetrieveNotifications(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = RetrieveNotificationSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        user = User.objects.get(email=user_data[0])
        notifications = Notifications.objects.filter(user_to_notify=user)
        print("THIS NOTIFICATION")
        print(notifications)
        return notifications

class MarkAsRead(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self,request,id):
        notification = Notifications.objects.get(id=id)
        notification.read_or_not_read = True
        notification.save()
        return Response({"message": "Notification Marked as read."}, status=status.HTTP_200_OK)

class OptIn_OptOut_Notifications(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self,request):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        user = User.objects.get(email=user_data[0])
        user.opt_in_for_notifications = not user.opt_in_for_notifications
        user.save()
        return Response({
            "message": "Opt in status for notifications is now changed to {}".format(user.opt_in_for_notifications)
            }, status=status.HTTP_200_OK)

        






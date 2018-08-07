from django.shortcuts import render
from rest_framework.views import APIView
from authors.apps.authentication.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from authors.settings.base import SECRET_KEY 
from authors.apps.authentication.backends import JWTAuthentication
import json
from authors.apps.profiles.serializers import (
    UpdateSerializer,ProfileSerializer
)

class UserUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateSerializer
    
    def check_empty_input(self,dictionary_input):
        for x in dictionary_input:
            if not dictionary_input[x]:
                return False
        return True
                
    
    def put(self,request):
        jwt = JWTAuthentication()
        if not self.check_empty_input(request.data):
            return Response(data={
                "error":"One of the input fields is empty."
                },status=status.HTTP_400_BAD_REQUEST)

        email = jwt.authenticate(request)[0]
        user = User.objects.filter(email=email)
        updated_user = self.serializer_class().update(user[0], request.data)
        return Response(data=self.serializer_class(updated_user).data,status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    def get(self,request):
        id = self.request.GET.get('id', None)
        if not id:
            return Response(data={
                "error":"The id was not supplied by the requesting url."
                },status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=self.request.GET.get('id', None))
        except User.DoesNotExist:
            return Response(data={
                "error":"This user id does not exist."
                },status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=self.serializer_class(user).data,status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta

from authors.settings.base import SECRET_KEY
from .models import User
import jwt
import os
from django.contrib.auth.hashers import make_password

from .renderers import UserJSONRenderer, FBAuthJSONRenderer, GoogleAuthJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, FacebookAPISerializer, GoogleAPISerializer,
)
from authors.apps.authentication.email_reg_util import SendAuthEmail
from authors.apps.authentication.reset_password_util import ResetPasswordUtil


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email_obj = SendAuthEmail()
        email_obj.send_reg_email(request,
                                 os.environ.get('EMAIL_HOST_USER'), serializer.data['email'], serializer.data['token'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerificationAPIView(UpdateAPIView):
    permission_classes = (AllowAny,)
    look_url_kwarg = 'token'

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get(self.look_url_kwarg)
        decoded_token = jwt.decode(token, SECRET_KEY, 'HS256')

        User.objects.filter(pk=decoded_token['id']).update(is_verified=True)
        user = User.objects.filter(pk=decoded_token['id']).values(
            'username', 'is_verified')

        user_dict = {'username': user[0]['username'],
                     'is_verified': user[0]['is_verified']}

        return Response(user_dict, status=status.HTTP_200_OK)


class SendPasswordResetEmailAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        dt = datetime.now()+timedelta(days=1)
        token = jwt.encode({'email': email, 'exp': int(
            dt.strftime('%s'))}, SECRET_KEY, 'HS256')
        email_obj = ResetPasswordUtil()
        email_obj.send_mail(request, os.environ.get(
            'EMAIL_HOST_USER'), email, token)
        return Response({'message': 'a link has been sent to your email.', 'token': token}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(UpdateAPIView):
    permission_classes = (AllowAny,)
    look_url_kwarg = 'token'

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get(self.look_url_kwarg)

        password = request.data.get('password')
        retyped_password = request.data.get('retyped_password')

        if password != retyped_password:
            raise Exception('Passwords do not match!')

        decoded_token = jwt.decode(token, SECRET_KEY, 'HS256')
        user = User.objects.get(email=decoded_token['email'])
        user.set_password(retyped_password)
        user.save()

        return Response({'message': 'your password has been changed.'}, status=status.HTTP_201_CREATED)


class FacebookLoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = FacebookAPISerializer
    renderer_classes = (FBAuthJSONRenderer,)

    def post(self,request, *args, **kwargs):
        user_data = request.data.get("user", {})
        serializer = self.serializer_class(data = user_data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class GoogleLoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = GoogleAPISerializer
    renderer_classes = (GoogleAuthJSONRenderer,)

    def post(self,request, *args, **kwargs):
        user_data = request.data.get("user", {})
        serializer = self.serializer_class(data = user_data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
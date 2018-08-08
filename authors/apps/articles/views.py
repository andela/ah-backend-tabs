from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from authors.apps.articles.serializers import CreateArticleSerializer, RateArticleSerializer,CreateCommentSerializer
from authors.apps.articles.renderers import ArticleJSONRenderer, RateArticleJSONRenderer,CommentJSONRenderer
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article,Comment
from rest_framework.permissions import IsAuthenticated
from authors.apps.authentication.backends import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import json

class ArticleCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def perform_create(self, serializer):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        serializer.save(author = user_data[0])

class RateArticleAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = RateArticleSerializer
    renderer_classes = (RateArticleJSONRenderer, )
    look_url_kwarg = "slug"

    def perform_create(self, serializer):
        slug = self.kwargs.get(self.look_url_kwarg)
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        serializer.save(user = user_data[0], article = get_object_or_404(Article, slug = slug))




    
class CommentCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateCommentSerializer
    renderer_classes = (CommentJSONRenderer,)
    look_url_kwarg = "slug"

    def perform_create(self, serializer):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        serializer.save(author = user_data[0], article = get_object_or_404(Article,slug=slug))

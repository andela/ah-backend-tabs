from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import CreateArticleSerializer, RateArticleSerializer
from .renderers import ArticleJSONRenderer, RateArticleJSONRenderer
from authors.apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated
from authors.apps.authentication.backends import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import Article
from rest_framework.views import APIView

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




    

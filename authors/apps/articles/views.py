from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import CreateArticleSerializer
from .renderers import ArticleJSONRenderer
from authors.apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated
from authors.apps.authentication.backends import JWTAuthentication

class ArticleCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def perform_create(self, serializer):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        serializer.save(author = user_data[0])

   
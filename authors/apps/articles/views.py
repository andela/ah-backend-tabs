from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from authors.apps.articles.serializers import CreateArticleSerializer, RateArticleSerializer,CreateCommentSerializer
from authors.apps.articles.renderers import ArticleJSONRenderer, RateArticleJSONRenderer,CommentJSONRenderer
from rest_framework.views import APIView
from .serializers import CreateArticleSerializer
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article,Comment
from rest_framework.permissions import IsAuthenticated
from authors.apps.authentication.backends import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from authors.apps.authentication.backends import JWTAuthentication

from rest_framework.response import Response
from rest_framework import status
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
class LikeArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "slug"


    def post(self,*args,**kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article,slug = slug)
        if article.likes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            return Response(data = {"errors":{"error":"Already liked"}},status=status.HTTP_409_CONFLICT)
        article.likes.add(user_data[0])
        article.likesCount+=1
        article.save()
        
        return Response(data = CreateArticleSerializer(article).data,status=status.HTTP_201_CREATED)

    def delete(self,*args,**kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article,slug = slug)
        if article.likes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.likes.remove(user_data[0])
            article.likesCount-=1
            article.save()
            return Response(data = CreateArticleSerializer(article).data,status=status.HTTP_200_OK)
        else:
            return Response(data = {"errors":{"error":"Not yet liked"}},status=status.HTTP_409_CONFLICT)
       

class DislikeArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "slug"


    def post(self,*args,**kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article,slug = slug)
        if article.dislikes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            return Response(data = {"errors":{"error":"Already disliked"}},status=status.HTTP_409_CONFLICT)
        
        if article.likes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.likes.remove(user_data[0])
        
        article.dislikes.add(user_data[0])
        article.dislikesCount+=1
        article.save()
        
        return Response(data = CreateArticleSerializer(article).data,status=status.HTTP_201_CREATED)

    def delete(self,*args,**kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article,slug = slug)
        if article.dislikes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.dislikes.remove(user_data[0])
            article.dislikesCount-=1
            article.save()
            return Response(data = CreateArticleSerializer(article).data,status=status.HTTP_200_OK)
        else:
            return Response(data = {"errors":{"error":"Not yet disliked"}},status=status.HTTP_409_CONFLICT)
       
class FavoriteArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "slug"


    def post(self,*args,**kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article,slug = slug)
        if article.favorites.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            return Response(data = {"errors":{"error":"Already favorited"}},status=status.HTTP_409_CONFLICT)
        article.favorites.add(user_data[0])
        article.favorited = True
        article.favoritesCount+=1
        article.save()
        
        return Response(data = CreateArticleSerializer(article).data,status=status.HTTP_201_CREATED)

    def delete(self,*args,**kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article,slug = slug)
        if article.favorites.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.favorites.remove(user_data[0])
            article.favoritesCount-=1
            if article.favoritesCount < 1:
                article.favorited = False
            article.save()
            return Response(data = CreateArticleSerializer(article).data,status=status.HTTP_200_OK)
        else:
            return Response(data = {"errors":{"error":"Not yet Favorited"}},status=status.HTTP_409_CONFLICT)
       


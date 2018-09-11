from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from authors.apps.articles.serializers import CreateArticleSerializer, RateArticleSerializer, CreateCommentSerializer, UpdateArticleSerializer
from authors.apps.articles.renderers import ArticleJSONRenderer, RateArticleJSONRenderer, CommentJSONRenderer, ListArticlesJSONRenderer
from rest_framework.views import APIView
from .serializers import CreateArticleSerializer
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Comment
from rest_framework.permissions import IsAuthenticated, AllowAny
from authors.apps.authentication.backends import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


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
        serializer.save(author=user_data[0])


class RateArticleAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = RateArticleSerializer
    renderer_classes = (RateArticleJSONRenderer, )
    look_url_kwarg = "slug"

    def perform_create(self, serializer):
        slug = self.kwargs.get(self.look_url_kwarg)
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        serializer.save(
            user=user_data[0], article=get_object_or_404(Article, slug=slug))


class CommentCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateCommentSerializer
    renderer_classes = (CommentJSONRenderer,)
    look_url_kwarg = "slug"

    def perform_create(self, serializer):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        serializer.save(
            author=user_data[0], article=get_object_or_404(Article, slug=slug))

class GetAllCommentsAPIView(ListAPIView):
    serializer_class = CreateCommentSerializer
    pagination_class = PageNumberPagination
    look_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.look_url_kwarg)
        article = Article.objects.filter(slug = slug)
        comments = article[0].user_comments.all()
        return comments

class LikeArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "slug"

    def post(self, *args, **kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article, slug=slug)
        if article.likes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            return Response(data={"errors": {"error": "Already liked"}}, status=status.HTTP_409_CONFLICT)
        article.likes.add(user_data[0])
        article.likesCount += 1
        article.save()

        return Response(data=CreateArticleSerializer(article).data, status=status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article, slug=slug)
        if article.likes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.likes.remove(user_data[0])
            article.likesCount -= 1
            article.save()
            return Response(data=CreateArticleSerializer(article).data, status=status.HTTP_200_OK)
        else:
            return Response(data={"errors": {"error": "Not yet liked"}}, status=status.HTTP_409_CONFLICT)


class DislikeArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "slug"

    def post(self, *args, **kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article, slug=slug)
        if article.dislikes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            return Response(data={"errors": {"error": "Already disliked"}}, status=status.HTTP_409_CONFLICT)

        if article.likes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.likes.remove(user_data[0])

        article.dislikes.add(user_data[0])
        article.dislikesCount += 1
        article.save()

        return Response(data=CreateArticleSerializer(article).data, status=status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article, slug=slug)
        if article.dislikes.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.dislikes.remove(user_data[0])
            article.dislikesCount -= 1
            article.save()
            return Response(data=CreateArticleSerializer(article).data, status=status.HTTP_200_OK)
        else:
            return Response(data={"errors": {"error": "Not yet disliked"}}, status=status.HTTP_409_CONFLICT)


class FavoriteArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = "slug"

    def post(self, *args, **kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article, slug=slug)
        if article.favorites.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            return Response(data={"errors": {"error": "Already favorited"}}, status=status.HTTP_409_CONFLICT)
        article.favorites.add(user_data[0])
        article.favorited = True
        article.favoritesCount += 1
        article.save()

        return Response(data=CreateArticleSerializer(article).data, status=status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        jwt = JWTAuthentication()
        user_data = jwt.authenticate(self.request)
        slug = self.kwargs.get(self.look_url_kwarg)
        article = get_object_or_404(Article, slug=slug)
        if article.favorites.filter(id=User.objects.filter(email=user_data[0])[0].id).exists():
            article.favorites.remove(user_data[0])
            article.favoritesCount -= 1
            if article.favoritesCount < 1:
                article.favorited = False
            article.save()
            return Response(data=CreateArticleSerializer(article).data, status=status.HTTP_200_OK)
        else:
            return Response(data={"errors": {"error": "Not yet Favorited"}}, status=status.HTTP_409_CONFLICT)


class SearchArticlesAPIView(ListAPIView):
    serializer_class = CreateArticleSerializer
    renderer_classes = (ListArticlesJSONRenderer,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Article.objects.all()
        if "title" in self.request.query_params:
            filter_field = self.request.query_params.get('title')
            filtered_queryset = queryset.filter(title__icontains=filter_field)

        if "author" in self.request.query_params:
            filter_field = self.request.query_params.get('author')
            user = get_object_or_404(User, username__icontains=filter_field)
            filtered_queryset = queryset.filter(author=user.id)

        if "slug" in self.request.query_params:
            filter_field = self.request.query_params.get('slug')
            filtered_queryset = queryset.filter(slug=filter_field)

        if "tag" in self.request.query_params:
            filter_field = self.request.query_params.get('tag')
            filtered_queryset = []
            if filter_field is not None:
                for article in queryset:
                    for tag in article.tags.all():
                        if filter_field == tag.name:
                            filtered_queryset.append(article)
        return filtered_queryset

class ListAllArticlesAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CreateArticleSerializer
    renderer_classes = (ListArticlesJSONRenderer,)
    pagination_class = PageNumberPagination
    def get_queryset(self):
        articles = Article.objects.all()
        return articles


class UpdateArticleAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdateArticleSerializer

    look_url_kwarg = 'slug'

    def put(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.look_url_kwarg)
        title = request.data.get('title')
        description = request.data.get('description')
        body = request.data.get('body')

        if not title:
            raise exceptions.APIException(
                detail='Please give the article a title.')
        elif not description:
            raise exceptions.APIException(
                'Please give the article a description.')
        elif not body:
            raise exceptions.APIException(
                'Please give the article a body.')
        try:
            article = Article.objects.filter(slug=slug)
            # article.update(title=title, description=description, body=body)
            updated_article = self.serializer_class().update(
                article[0], request.data)
        except Exception as e:
            raise exceptions.APIException(e)

        return Response(data=self.serializer_class(updated_article).data, status=status.HTTP_201_CREATED)


class DeleteArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    look_url_kwarg = 'slug'

    def delete(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.look_url_kwarg)
        
        article = Article.objects.filter(slug=slug).delete()

        if article[0] == 0:
            return Response({'message': 'Operation was not performed, no such article found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Article deleted.'}, status=status.HTTP_200_OK)

from django.urls import path

from .views import (
    ArticleCreateAPIView, 
    RateArticleAPIView,
    CommentCreateAPIView,
    LikeArticleAPIView,
    DislikeArticleAPIView,
    FavoriteArticleAPIView
)


app_name = "articles"

urlpatterns = [
    path('articles', ArticleCreateAPIView.as_view()),
    path('articles/<slug>/rate/', RateArticleAPIView.as_view()),
    path('articles/<slug>/comment', CommentCreateAPIView.as_view()),
    path('articles/<slug>/like',LikeArticleAPIView.as_view()),
    path('articles/<slug>/dislike',DislikeArticleAPIView.as_view()),
    path('articles/<slug>/favorite',FavoriteArticleAPIView.as_view()),
]


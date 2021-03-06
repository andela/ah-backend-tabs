from django.urls import path

from .views import (
    ArticleCreateAPIView,
    RateArticleAPIView,
    CommentCreateAPIView,
    LikeArticleAPIView,
    DislikeArticleAPIView,
    FavoriteArticleAPIView,
    UpdateArticleAPIView,
    SearchArticlesAPIView,
    DeleteArticleAPIView,
    ListAllArticlesAPIView,
    GetAllCommentsAPIView,
    GetLikesandDislikesAPIView,
    GetArticleAverageRatingAPIView,
    ArticleTextCommentCreateAPIView,
    GetAllArticleTextCommentsAPIView
)

app_name = "articles"

urlpatterns = [
    path('articles', ArticleCreateAPIView.as_view()),
    path('articles/<slug>/rate/', RateArticleAPIView.as_view()),
    path('articles/<slug>/comment', CommentCreateAPIView.as_view()),
    path('articles/<slug>/update/', UpdateArticleAPIView.as_view()),
    path('articles/<slug>/like', LikeArticleAPIView.as_view()),
    path('articles/<slug>/dislike', DislikeArticleAPIView.as_view()),
    path('articles/<slug>/favorite', FavoriteArticleAPIView.as_view()),
    path('articles/search', SearchArticlesAPIView.as_view()),
    path('articles/<slug>/delete/', DeleteArticleAPIView.as_view()),
    path('articles/all/', ListAllArticlesAPIView.as_view()),
    path('articles/<slug>/all/comments/', GetAllCommentsAPIView.as_view()),
    path('articles/<slug>/likes/dislikes/', GetLikesandDislikesAPIView.as_view()),
    path('articles/<slug>/average-rating/', GetArticleAverageRatingAPIView.as_view()),
    path('articles/<slug>/text-comment/', ArticleTextCommentCreateAPIView.as_view()),
    path('articles/<slug>/all/text-comments/', GetAllArticleTextCommentsAPIView.as_view()),
]

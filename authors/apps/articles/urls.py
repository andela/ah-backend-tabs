from django.urls import path

from .views import ArticleCreateAPIView, RateArticleAPIView

app_name = "articles"

urlpatterns = [
    path('articles', ArticleCreateAPIView.as_view()),
    path('articles/<slug>/rate/', RateArticleAPIView.as_view()),

]

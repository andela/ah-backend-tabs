from django.urls import path

from .views import ArticleCreateAPIView

app_name = "articles"

urlpatterns = [
    path('articles', ArticleCreateAPIView.as_view()),
]

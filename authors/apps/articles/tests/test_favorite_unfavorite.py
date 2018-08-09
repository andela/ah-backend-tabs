from django.test import TestCase, RequestFactory
from authors.apps.articles.views import ArticleCreateAPIView,FavoriteArticleAPIView
from authors.apps.authentication.views import LoginAPIView
from rest_framework.test import force_authenticate
from authors.apps.authentication.models import User
import json

class FavoriteUnfavoriteTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user" : {
            "email":"test@gmail.com",
            "username":"tester",
            "password":"testpass@word"
        }
        }

        user = User.objects.create_user(self.user["user"]["username"], self.user["user"]["email"], self.user["user"]["password"])
        user.is_verified = True
        user.save()

        self.article_data = {
                "title":"How to Survive",
                "description":"How?",
                "body":"This is how to survive"
            }

        self.request = self.factory.post('/api/users/login/', data = json.dumps(self.user), content_type='application/json')
        self.response = LoginAPIView.as_view()(self.request)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response.data["token"]
        }
        

        request = self.factory.post('api/articles', data = json.dumps(self.article_data), **self.headers, content_type = 'application/json')
        response = ArticleCreateAPIView.as_view()(request)

    def test_favorite_normal(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/favorite', **self.headers)
        response = FavoriteArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 201)

    def test_favorite_missing_slug(self):
        request = self.factory.post('api/articles/favorite', **self.headers)
        response = FavoriteArticleAPIView.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_favorite_already_favorited(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/factory', **self.headers)
        response = FavoriteArticleAPIView.as_view()(request,**kwargs)
        response = FavoriteArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 409)

    def test_unfavorite_normal(self):
        kwargs = {"slug":"how-to-survive"}
        FavoriteArticleAPIView.as_view()(self.factory.post('api/articles/how-to-survive/favorite', **self.headers),**kwargs)
        request = self.factory.delete('api/articles/how-to-survive/factory', **self.headers)
        response = FavoriteArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_unfavorite_before_favorite(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.delete('api/articles/how-to-survive/favorite', **self.headers)
        response = FavoriteArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 409)

    def test_unfavorite_missing_slug(self):
        request = self.factory.delete('api/articles/favorite', **self.headers)
        response = FavoriteArticleAPIView.as_view()(request)
        self.assertEqual(response.status_code, 404)

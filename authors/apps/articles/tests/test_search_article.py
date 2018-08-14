from django.test import TestCase, RequestFactory
from authors.apps.articles.views import (
    ArticleCreateAPIView,
    SearchArticlesAPIView,
)
from authors.apps.authentication.views import LoginAPIView
from rest_framework.test import force_authenticate
from authors.apps.authentication.models import User
import json

class SearchArticleTestCase(TestCase):
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
                "body":"This is how to survive",
                "tags":["test"]
            }

        self.request = self.factory.post('/api/users/login/', data = json.dumps(self.user), content_type='application/json')
        self.response = LoginAPIView.as_view()(self.request)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response.data["token"]
        }
        

        request = self.factory.post('api/articles', data = json.dumps(self.article_data), **self.headers, content_type = 'application/json')
        response = ArticleCreateAPIView.as_view()(request)

    def test_search_by_author_normal(self):
        request = self.factory.get('api/articles/search?author=tester')
        response = SearchArticlesAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_search_by_author_non_existent(self):
        request = self.factory.get('api/articles/search?author=non-existent')
        response = SearchArticlesAPIView.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_search_by_title_normal(self):
        request = self.factory.get('api/articles/search?title=How')
        response = SearchArticlesAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_search_by_title_non_existent(self):
        request = self.factory.get('api/articles/search?title=XYZ')
        response = SearchArticlesAPIView.as_view()(request)
        self.assertEqual(response.data["count"], 0)

    def test_search_by_tag_normal(self):
            request = self.factory.get('api/articles/search?tag=test')
            response = SearchArticlesAPIView.as_view()(request)
            self.assertGreater(response.data["count"], 0)

    def test_search_by_tag_non_existent(self):
        request = self.factory.get('api/articles/search?tag=XYZ')
        response = SearchArticlesAPIView.as_view()(request)
        self.assertEqual(response.data["count"], 0)
        
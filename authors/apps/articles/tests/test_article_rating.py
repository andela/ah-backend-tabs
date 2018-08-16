from django.test import TestCase, RequestFactory
from authors.apps.articles.views import ArticleCreateAPIView, RateArticleAPIView
from authors.apps.authentication.views import RegistrationAPIView
from authors.apps.articles.models import Article, Rating
from django.shortcuts import get_object_or_404
import json
from authors.apps.utils.app_util import UtilClass


class RateArticleTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user" : {
            "email":"test@gmail.com",
            "username":"tester",
            "password":"testpass@word"
        }
        }

        self.user_two = {
            "user" : {
            "email":"test2@gmail.com",
            "username":"tester2",
            "password":"testpass@word"
        }
        }

        self.obj = UtilClass()
        registered_user = self.obj.get_reg_data(self.user)
        self.obj.verify_user({"token":registered_user.data["token"]})
        logged_in_user = self.obj.get_login_data(self.user)

        registered_user_two = self.obj.get_reg_data(self.user_two)
        self.obj.verify_user({"token":registered_user_two.data["token"]})
        logged_in_user_two = self.obj.get_login_data(self.user_two)

        self.request = self.factory.post('/api/users/', data = json.dumps(self.user), content_type='application/json')
       
        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + logged_in_user.data["token"]
        }

        
        self.headers_two = {
            'HTTP_AUTHORIZATION': 'Token ' + logged_in_user_two.data["token"]
        }

        self.article_data = {
            "title": "This is Postman",
            "description": "Hello Postman",
            "body": "Hahahaha",
            "tags": ["post","man"]
        }

        article_create_request = self.factory.post('api/articles', data = json.dumps(self.article_data), **self.headers, content_type = 'application/json')
        ArticleCreateAPIView.as_view()(article_create_request)

        self.kwargs = {"slug":"this-is-postman"}

    def test_article_rating_successful(self):
        request = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({"amount":4}), **self.headers, content_type = 'application/json')
        response = RateArticleAPIView.as_view()(request,  **self.kwargs)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["amount"],4)

    def test_article_rating_missing_rate(self):
        request = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({}), **self.headers, content_type = 'application/json')
        response = RateArticleAPIView.as_view()(request,  **self.kwargs)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['amount'][0],"This field is required.")

    def test_change_article_rating_(self):
        request = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({"amount":4}), **self.headers, content_type = 'application/json')
        response = RateArticleAPIView.as_view()(request,  **self.kwargs)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['amount'],4)

        request_two = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({"amount":3}), **self.headers, content_type = 'application/json')
        response_two = RateArticleAPIView.as_view()(request_two,  **self.kwargs)
        self.assertEqual(response_two.status_code, 201)
        self.assertEqual(response_two.data['amount'],3)

    def test_only_one_user_rating_per_article(self):
        request = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({"amount":4}), **self.headers, content_type = 'application/json')
        response = RateArticleAPIView.as_view()(request,  **self.kwargs)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['amount'],4)

        request_two = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({"amount":3}), **self.headers, content_type = 'application/json')
        response_two = RateArticleAPIView.as_view()(request_two,  **self.kwargs)
        self.assertEqual(response_two.status_code, 201)
        self.assertEqual(response_two.data['amount'],3)

        ratings = Rating.objects.all()
        self.assertEqual(len(ratings),1)

    def test_average_rating_for_article(self):
        request = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({"amount":5}), **self.headers, content_type = 'application/json')
        response = RateArticleAPIView.as_view()(request,  **self.kwargs)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['amount'],5)

        request_two = self.factory.post('api/articles/this-is-postman/rate/',data = json.dumps({"amount":1}), **self.headers_two, content_type = 'application/json')
        response_two = RateArticleAPIView.as_view()(request_two,  **self.kwargs)
        self.assertEqual(response_two.status_code, 201)
        self.assertEqual(response_two.data['amount'],1)

        article = get_object_or_404(Article, slug = self.kwargs["slug"])
        self.assertEqual(article.rating, 3)


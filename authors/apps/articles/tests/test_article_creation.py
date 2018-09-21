from django.test import TestCase, RequestFactory
from authors.apps.articles.views import ArticleCreateAPIView
from authors.apps.authentication.views import RegistrationAPIView, VerificationAPIView
import json
import smtplib
from minimock import Mock
from authors.apps.utils.app_util import UtilClass


class CreateArticleTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word",
                "callbackurl": ""
            }
        }
        self.obj = UtilClass()
        registered_user = self.obj.get_reg_data(self.user)
        self.obj.verify_user({"token": registered_user.data["token"]})
        logged_in_user = self.obj.get_login_data(self.user)

        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + logged_in_user.data["token"]
        }

        self.article_data = {
            "title": "This is Postman",
            "description": "Hello Postman",
            "body": "Hahahaha",
            "tags": ["post", "man"]
        }

    def test_article_created_successful(self):

        request = self.factory.post('api/articles', data=json.dumps(
            self.article_data), **self.headers, content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        self.assertEqual("This is Postman", response.data["title"])
        self.assertEqual(
            {"username": "tester", "email": "test@gmail.com", "bio": "","image":""}, response.data["author"])
        self.assertEqual(2, len(response.data["tags"]))
        self.assertEqual(response.status_code, 201)

    def test_article_creation_with_blank_title(self):
        article_data = {
            "title": "",
            "description": "Hello Postman",
            "body": "Hahahaha",
            "tags": ["post", "man"]
        }

        request = self.factory.post('api/articles', data=json.dumps(
            article_data), **self.headers, content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        self.assertEqual("This field may not be blank.",
                         response.data["errors"]["title"][0])
        self.assertEqual(response.status_code, 400)

    def test_article_creation_with_missing_description(self):
        article_data = {
            "title": "This is Postman",
            "body": "Hahahaha",
            "tags": ["post", "man"]
        }

        request = self.factory.post('api/articles', data=json.dumps(
            article_data), **self.headers, content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        self.assertEqual("This field is required.",
                         response.data["errors"]["description"][0])
        self.assertEqual(response.status_code, 400)

    def test_article_creation_with_missing_body(self):
        article_data = {
            "title": "This is Postman",
            "description": "Hello Postman",
            "tags": ["post", "man"]
        }

        request = self.factory.post('api/articles', data=json.dumps(
            article_data), **self.headers, content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        self.assertEqual("This field is required.",
                         response.data["errors"]["body"][0])
        self.assertEqual(response.status_code, 400)

    def test_article_creation_without_auth_credentials(self):
        request = self.factory.post(
            'api/articles', data=json.dumps(self.article_data), content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        self.assertEqual(
            "Authentication credentials were not provided.", response.data["detail"])
        self.assertEqual(response.status_code, 403)

    def test_article_creation_with_bad_auth_credentials(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + "invalid_token"
        }
        request = self.factory.post('api/articles', data=json.dumps(
            self.article_data), **headers, content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        self.assertEqual("Authentication failed!", response.data["detail"])
        self.assertEqual(response.status_code, 403)

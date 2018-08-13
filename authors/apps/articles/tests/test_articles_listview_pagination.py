from django.test import TestCase, RequestFactory
from authors.apps.articles.views import ArticleCreateAPIView,ListAuthorArticlesAPIView,ListFollowingArticlesAPIView
from authors.apps.authentication.views import RegistrationAPIView, VerificationAPIView
import json
import smtplib
from minimock import Mock


class ArticleListPaginationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }

        self.user_two = {
            "user": {
                "email": "test2@gmail.com",
                "username": "tester2",
                "password": "testpass@word"
            }
        }
        smtplib.SMTP = Mock('smtplib.SMTP', tracker=None)
        smtplib.SMTP.mock_returns = Mock('smtp_connection')

        self.request = self.factory.post(
            '/api/users/', data=json.dumps(self.user), content_type='application/json')
        self.response = RegistrationAPIView.as_view()(self.request)

        self.request_two = self.factory.post(
            '/api/users/', data=json.dumps(self.user_two), content_type='application/json')
        self.response_two = RegistrationAPIView.as_view()(self.request_two)

        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response.data["token"]
        }

        self.headers_two = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response_two.data["token"]
        }

        verfication_request = self.factory.put(
            '/api/users/verify/token', content_type='application/json')
        VerificationAPIView.as_view()(verfication_request, **
                                      {"token": self.response.data["token"]})

        VerificationAPIView.as_view()(verfication_request, **
                                      {"token": self.response_two.data["token"]})

        self.article_data = {
            "title": "This is Postman",
            "description": "Hello Postman",
            "body": "Hahahaha",
            "tags": ["post", "man"]
        } 
        

        x = 0
        while x < 7:
            request = self.factory.post('api/articles', data=json.dumps(self.article_data), **self.headers, content_type='application/json')
            ArticleCreateAPIView.as_view()(request)
            x = x + 1

        y = 0
        while y < 8:
            request_two = self.factory.post('api/articles', data=json.dumps(self.article_data), **self.headers_two, content_type='application/json')
            ArticleCreateAPIView.as_view()(request_two)
            y = y + 1


    def test_my_articles_listview_pagination(self):
        request = self.factory.get('api/my/articles/',**self.headers, content_type = 'application/json')
        response = ListAuthorArticlesAPIView.as_view()(request)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.status_code, 200)

        request_second_page = self.factory.get('api/my/articles/?page=2',**self.headers, content_type = 'application/json')
        response_second_page = ListAuthorArticlesAPIView.as_view()(request_second_page)
        self.assertEqual(len(response_second_page.data["results"]), 2)
        self.assertEqual(response.status_code, 200)

    def test_author_articles_listview_pagination(self):
        request = self.factory.get('api/tester2/articles/',**self.headers, content_type = 'application/json')
        response = ListFollowingArticlesAPIView.as_view()(request, **{"username":"tester2"})
        print(response.data)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.status_code, 200)

        request_second_page = self.factory.get('api/tester2/articles/?page=2',**self.headers, content_type = 'application/json')
        response_second_page = ListFollowingArticlesAPIView.as_view()(request_second_page, **{"username":"tester2"})
        self.assertEqual(len(response_second_page.data["results"]), 3)
        self.assertEqual(response.status_code, 200)







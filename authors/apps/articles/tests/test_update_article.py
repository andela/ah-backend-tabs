from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import RegistrationAPIView, VerificationAPIView
from authors.apps.articles.views import UpdateArticleAPIView, ArticleCreateAPIView
import json
from minimock import Mock
import smtplib
from rest_framework import exceptions, authentication


class UpdateArticleTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')
        self.article = {
            'title': 'original title',
            'description': 'original description',
            'body': 'original body'
        }
        self.update_article = {
            'title': 'updated title',
            'description': 'updated description',
            'body': 'updated body'
        }
        self.user = {'user': {'email': 'allan.guwatudde@andela.com',
                              'username': 'testusername7',
                              'password': 'testpassword1234567#'
                              }
                     }
        self.token = self.make_token(self.user)
        self.kwargs = {'token': self.token}
        self.verify_user()
        self.slug = self.create_article()

    def make_token(self, user):
        request = self.factory.post(
            '/api/users/', data=json.dumps(user), content_type='application/json')
        response = RegistrationAPIView.as_view()(request)
        return response.data['token']

    def verify_user(self):
        request = self.factory.post(
            '/api/users/verify/', content_type='application/json')
        VerificationAPIView.as_view()(request, **self.kwargs)

    def create_article(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        request = self.factory.post(
            '/api/articles/', **headers, data=json.dumps(self.article), content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        return response.data['slug']

    def test_update_article(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        request = self.factory.put(
            'articles/<slug>/update/', data=json.dumps(self.update_article), **headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        self.assertEqual(self.update_article, response.data)

    def test_no_title(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        update_article = {
            'description': 'updated description',
            'body': 'updated body'
        }
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            update_article), **headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        print(response.data)
        self.assertEqual(response.data['detail'],
                         'Please give the article a title.')

    def test_no_description(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        update_article = {
            'title': 'updated title',
            'body': 'updated body'
        }
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            update_article), **headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        print(response.data)
        self.assertEqual(response.data['detail'],
                         'Please give the article a description.')

    def test_no_body(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        update_article = {
            'title': 'updated title',
            'description': 'updated description',
        }
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            update_article), **headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        print(response.data)
        self.assertEqual(response.data['detail'],
                         'Please give the article a body.')

    def test_non_article(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            self.update_article), **headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': 'hgsfkjgygfhjdgfhjbrgfgdfhghj'})
        print(response.data)
        self.assertEqual(response.data['detail'], 'list index out of range')

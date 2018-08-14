from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import RegistrationAPIView, VerificationAPIView
from authors.apps.articles.views import (
    UpdateArticleAPIView,
    ArticleCreateAPIView,
    DeleteArticleAPIView,)
import json
from minimock import Mock
import smtplib
from rest_framework import exceptions, authentication


class DeleteArticleTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')
        self.article = {
            'title': 'original title',
            'description': 'original description',
            'body': 'original body'
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

    def test_delete_article(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        request = self.factory.delete(
            '/api/article/<slug>/delete', **headers, content_type='application/json')
        response = DeleteArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        self.assertEqual(response.data['message'], 'Article deleted.')
        self.assertEqual(response.status_code, 200)

    def test_delete_non_article(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        request = self.factory.delete(
            '/api/article/<slug>/delete', **headers, content_type='application/json')
        response = DeleteArticleAPIView.as_view()(
            request, **{'slug': 'uyfuygbhcbyegfyuergbhybcvyqegbfgygbdhbfefbfbccvyvfe'})
        self.assertEqual(
            response.data['message'], 'Operation was not performed, no such article found.')
        self.assertEqual(response.status_code, 404)

    def test_delete_for_missing_slug(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token
        }
        request = self.factory.delete(
            '/api/article/<slug>/delete', **headers, content_type='application/json')
        response = DeleteArticleAPIView.as_view()(
            request, **{'slug': ''})
        self.assertEqual(
            response.data['message'], 'Operation was not performed, no such article found.')
        self.assertEqual(response.status_code, 404)

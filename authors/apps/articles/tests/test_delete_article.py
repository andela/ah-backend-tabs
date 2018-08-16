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
from authors.apps.utils.app_util import UtilClass


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

        self.obj = UtilClass()
        registered_user = self.obj.get_reg_data(self.user)
        self.obj.verify_user({"token":registered_user.data["token"]})
        logged_in_user = self.obj.get_login_data(self.user)

        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + logged_in_user.data["token"]
        }

        self.slug = self.create_article()

    
    def create_article(self):
        request = self.factory.post(
            '/api/articles/', **self.headers, data=json.dumps(self.article), content_type='application/json')
        response = ArticleCreateAPIView.as_view()(request)
        return response.data['slug']

    def test_delete_article(self):
        request = self.factory.delete(
            '/api/article/<slug>/delete', **self.headers, content_type='application/json')
        response = DeleteArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        self.assertEqual(response.data['message'], 'Article deleted.')
        self.assertEqual(response.status_code, 200)

    def test_delete_non_article(self):
        request = self.factory.delete(
            '/api/article/<slug>/delete', **self.headers, content_type='application/json')
        response = DeleteArticleAPIView.as_view()(
            request, **{'slug': 'uyfuygbhcbyegfyuergbhybcvyqegbfgygbdhbfefbfbccvyvfe'})
        self.assertEqual(
            response.data['message'], 'Operation was not performed, no such article found.')
        self.assertEqual(response.status_code, 404)

    def test_delete_for_missing_slug(self):
        request = self.factory.delete(
            '/api/article/<slug>/delete', **self.headers, content_type='application/json')
        response = DeleteArticleAPIView.as_view()(
            request, **{'slug': ''})
        self.assertEqual(
            response.data['message'], 'Operation was not performed, no such article found.')
        self.assertEqual(response.status_code, 404)

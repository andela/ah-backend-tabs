from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import RegistrationAPIView, VerificationAPIView
from authors.apps.articles.views import UpdateArticleAPIView, ArticleCreateAPIView
import json
from minimock import Mock
import smtplib
from rest_framework import exceptions, authentication
from authors.apps.utils.app_util import UtilClass


class UpdateArticleTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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

    def test_update_article(self):
        request = self.factory.put(
            'articles/<slug>/update/', data=json.dumps(self.update_article), **self.headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        self.assertEqual(self.update_article, response.data)

    def test_no_title(self):
        update_article = {
            'description': 'updated description',
            'body': 'updated body'
        }
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            update_article), **self.headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})

        self.assertEqual(response.data['detail'],
                         'Please give the article a title.')

    def test_no_description(self):
        update_article = {
            'title': 'updated title',
            'body': 'updated body'
        }
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            update_article), **self.headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        print(response.data)
        self.assertEqual(response.data['detail'],
                         'Please give the article a description.')

    def test_no_body(self):
        update_article = {
            'title': 'updated title',
            'description': 'updated description',
        }
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            update_article), **self.headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': self.slug})
        print(response.data)
        self.assertEqual(response.data['detail'],
                         'Please give the article a body.')

    def test_non_article(self):
        request = self.factory.put('articles/<slug>/update/', data=json.dumps(
            self.update_article), **self.headers, content_type='application/json')
        response = UpdateArticleAPIView.as_view()(
            request, **{'slug': 'hgsfkjgygfhjdgfhjbrgfgdfhghj'})
        print(response.data)
        self.assertEqual(response.data['detail'], 'list index out of range')

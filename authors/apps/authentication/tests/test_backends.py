from django.test import TestCase, RequestFactory
from authors.apps.authentication.backends import JWTAuthentication
from authors.apps.authentication.models import User, UserManager
from authors.apps.authentication.views import LoginAPIView, RegistrationAPIView
import json
import jwt
from datetime import timedelta, datetime
from authors.settings.base import SECRET_KEY
from rest_framework import authentication, exceptions
from minimock import Mock
import smtplib


class BackendsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.auth_obj = JWTAuthentication()
        self.user = {
            "user": {
                "email": "phillip.seryazi@andela.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')

    def make_token(self, user):
        request = self.factory.post(
            '/api/users/', data=json.dumps(user), content_type='application/json')
        response = RegistrationAPIView.as_view()(request)
        return response.data['token']

    def test_token_validity(self):
        request = self.factory.post(
            '/api/users/', content_type='application/json', data=json.dumps(self.user))
        response = RegistrationAPIView.as_view()(request)
        self.assertEquals(
            self.user['user']['username'], response.data['username'])

    def test_no_auth_header_on_request(self):
        request = self.factory.post(
            '/api/users/', content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        self.assertEquals(None, response)

    def test_auth_array_size_is_equal_to_one(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token '
        }
        request = self.factory.post(
            '/api/users/', **headers, content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        self.assertEqual(None, response)

    def test_auth_array_size_is_greater_than_two(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token Bearer ' + self.make_token(self.user)
        }
        request = self.factory.post(
            '/api/users/', **headers, content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        self.assertEqual(None, response)

    def test_token_prefix_validity(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.make_token(self.user)
        }
        request = self.factory.post(
            '/api/users/', **headers, content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        self.assertEqual(None, response)

    def test_authenticate_method(self):
        token = self.make_token(self.user)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + token
        }
        request = self.factory.post(
            '/api/users/', **headers, content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        expected_response = (response[0], token)
        self.assertEqual(response, expected_response)

    def test_authentication_failed(self):
        dt = datetime.now()+timedelta(days=1)
        token = jwt.encode({
            'id': 1,
            'exp': int(dt.strftime('%s')),
            'username': self.user['user']['username'],
            'email': self.user['user']['email']
        }, 'brooogfghf', algorithm='HS256')
        request = self.factory.post(
            '/api/users/', content_type='application/json', data=json.dumps(self.user))
        with self.assertRaises(Exception) as context:
            self.auth_obj._authenticate_credentials(request, token)
        self.assertIn('Authentication failed!', str(context.exception))

    def test_user_not_recognised(self):
        dt = datetime.now()+timedelta(days=1)
        token = jwt.encode({
            'id': 2,
            'exp': int(dt.strftime('%s')),
            'username': self.user['user']['username'],
            'email': self.user['user']['email']
        }, SECRET_KEY, algorithm='HS256')
        request = self.factory.post(
            '/api/users/', content_type='application/json', data=json.dumps(self.user))
        with self.assertRaises(Exception) as context:
            self.auth_obj._authenticate_credentials(request, token)
        self.assertIn('User not recognised!', str(context.exception))

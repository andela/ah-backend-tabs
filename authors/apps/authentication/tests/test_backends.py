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
from authors.apps.utils.app_util import UtilClass

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

        self.obj = UtilClass()
        registered_user = self.obj.get_reg_data(self.user)
        self.obj.verify_user({"token":registered_user.data["token"]})
        self.logged_in_user = self.obj.get_login_data(self.user)

        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.logged_in_user.data["token"]
        }


    def test_token_validity(self):
        request = self.factory.post(
            '/api/users/', content_type='application/json', data=json.dumps(self.user))
        response = self.logged_in_user
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
            'HTTP_AUTHORIZATION': 'Token Bearer ' + self.logged_in_user.data["token"]
        }
        request = self.factory.post(
            '/api/users/', **headers, content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        self.assertEqual(None, response)

    def test_token_prefix_validity(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.logged_in_user.data["token"]
        }
        request = self.factory.post(
            '/api/users/', **headers, content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        self.assertEqual(None, response)

    def test_authenticate_method(self):
        request = self.factory.post(
            '/api/users/', **self.headers, content_type='application/json', data=json.dumps(self.user))
        response = self.auth_obj.authenticate(request)
        expected_response = (response[0], self.logged_in_user.data["token"])
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

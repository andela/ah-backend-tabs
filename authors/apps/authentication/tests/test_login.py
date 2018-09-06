from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import LoginAPIView, RegistrationAPIView, VerificationAPIView
from authors.apps.utils.app_util import UtilClass
import json
from minimock import Mock
import smtplib


class LoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = {
            "user": {
                "email": "rutale@gmail.com",
                "password": "rutale1234*",
                "username": "rutale",
                "callbackurl":""
            }
        }
        self.obj = UtilClass()
        self.reg_data = self.obj.get_reg_data(self.user)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.reg_data.data['token']
        }
        self.kwargs = {'token': self.reg_data.data['token']}
        self.obj.verify_user(self.kwargs)

    def test_normal_login(self):
        response = self.obj.get_login_data(self.user)
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_email(self):
        user = {
            'user': {
                'email': 'rut@gmail.com',
                'password': 'rutale1234*'
            }
        }
        response = self.obj.get_login_data(user)
        self.assertIn('A user with this email and password was not found.',
                      response.data["errors"]["error"][0])
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_password(self):
        user = {
            'user': {
                'email': 'rutale@gmail.com',
                'password': 'rutale123'
            }
        }
        response = self.obj.get_login_data(user)
        self.assertEqual(response.status_code, 400)

    def test_login_missing_email(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': '',
                'password': 'rutale1234*'
            }
        }
        response = self.obj.get_login_data(user)
        self.assertIn('This field may not be blank.',
                      response.data["errors"]["email"][0])
        self.assertEqual(response.status_code, 400)

    def test_login_missing_password(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
                'password': ''
            }
        }
        response = self.obj.get_login_data(user)
        self.assertIn('This field may not be blank.',
                      response.data["errors"]["password"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_email_index(self):
        user = {
            'user': {
                'username': 'rutale',
                '': 'rut@gmail.com',
                'password': 'rutale1234*'
            }
        }
        response = self.obj.get_login_data(user)
        self.assertIn('This field is required.',
                      response.data["errors"]["email"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_password_index(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
                '': 'rutaleivan'
            }
        }
        response = self.obj.get_login_data(user)
        self.assertIn('This field is required.',
                      response.data["errors"]["password"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_password_field(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
            }
        }
        response = self.obj.get_login_data(user)
        self.assertIn('This field is required.',
                      response.data["errors"]["password"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_email_field(self):
        user = {
            'user': {
                'username': 'rutale',
                'password': 'rutale1234*'
            }
        }
        response = self.obj.get_login_data(user)
        self.assertIn('This field is required.',
                      response.data["errors"]["email"][0])
        self.assertEqual(response.status_code, 400)

    def test_datastructure_user_error_missing_username_field(self):
        user = {
            'user': {
                'email': 'rutale@gmail.com',
                'password': 'rutale1234*'
            }
        }
        response = self.obj.get_login_data(user)
        self.assertEqual(response.status_code, 200)

from django.test import TestCase, RequestFactory
import json
import jwt
from authors.apps.authentication.views import SendPasswordResetEmailAPIView, ResetPasswordAPIView, RegistrationAPIView
from minimock import Mock
import smtplib


class ResetPasswordTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }
        self.email_dict = {'email': 'teste@gmail.com'}
        self.password_dict = {'password': 'password1234567#',
                              'retyped_password': 'password1234567#'}

        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')

        self.request = self.factory.post(
            'users/password/forgot/', data=json.dumps(self.email_dict), content_type='application/json')
        self.response = SendPasswordResetEmailAPIView.as_view()(self.request)

        """create user in database"""
        self.reg_request = self.factory.post(
            '/api/users/', data=json.dumps(self.user), content_type='application/json')
        self.reg_response = RegistrationAPIView.as_view()(self.reg_request)
        self.kwargs = {'token': self.reg_response.data['token']}

    def test_send_reset_mail(self):
        self.assertEqual(self.response.status_code, 200)

    def test_reset_password(self):
        self.request = self.factory.put(
            'users/password/reset/', data=json.dumps(self.password_dict), content_type='application/json')
        self.response = ResetPasswordAPIView.as_view()(self.request, **self.kwargs)
        self.assertEqual(self.response.status_code, 201)

    def test_mismatched_password(self):
        password_dict = {'password': 'password12345687#',
                         'retyped_password': '1234567#password'}
        with self.assertRaises(Exception) as context:
            self.request = self.factory.put(
                'users/password/reset/', data=json.dumps(password_dict), content_type='application/json')
            self.response = ResetPasswordAPIView.as_view()(self.request, **self.kwargs)
        self.assertIn('Passwords do not match!', str(context.exception))

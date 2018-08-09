from django.test import TestCase, RequestFactory
import json
import jwt
from authors.apps.authentication.models import User, UserManager
from authors.apps.authentication.views import LoginAPIView, RegistrationAPIView, VerificationAPIView
from minimock import Mock
import smtplib


class TestVerification(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }
        self.kwargs = {'token': self.make_token(self.user)}
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')

    def make_token(self, user):
        request = self.factory.post(
            '/api/users/', data=json.dumps(user), content_type='application/json')
        response = RegistrationAPIView.as_view()(request)
        return response.data['token']

    def test_verification(self):
        request = self.factory.put(
            '/api/users/verify/', content_type='application/json')
        response = VerificationAPIView.as_view()(request, **self.kwargs)
        expected_reponse = {
            'username': self.user['user']['username'], 'is_verified': True}
        self.assertEqual(response.data, expected_reponse)
        self.assertEqual(response.status_code, 200)

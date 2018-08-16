from django.test import TestCase, RequestFactory
import json
import jwt
from authors.apps.authentication.models import User, UserManager
from authors.apps.authentication.views import LoginAPIView, RegistrationAPIView, VerificationAPIView
from authors.apps.utils.app_util import UtilClass
from minimock import Mock
import smtplib


class TestVerification(TestCase):
    def setUp(self):
        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }
        self.obj = UtilClass()
        token = self.obj.get_reg_data(self.user)
        self.kwargs = {'token': token.data['token']}

    def test_verification(self):
        response = self.obj.verify_user(self.kwargs)
        expected_reponse = {
            'username': self.user['user']['username'], 'is_verified': True}
        self.assertEqual(response, expected_reponse)

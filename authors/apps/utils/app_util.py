from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import (
    RegistrationAPIView, VerificationAPIView, LoginAPIView)
import json
from minimock import Mock
import smtplib


class UtilClass():
    def __init__(self):
        self.factory = RequestFactory()
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')

    def get_reg_data(self, user):
        request = self.factory.post(
            '/api/users/', data=json.dumps(user), content_type='application/json')
        response = RegistrationAPIView.as_view()(request)
        return response

    def verify_user(self, kwargs={}):
        request = self.factory.put(
            '/api/users/verify/', content_type='application/json')
        response = VerificationAPIView.as_view()(request, **kwargs)
        return response.data

    def get_login_data(self, user):
        request = self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        return response

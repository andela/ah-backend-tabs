from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import GoogleLoginAPIView
from authors.apps.authentication.models import User
import json

class GoogleLoginTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.google_wrong_token_body = {
            "user":{
                "googleauth_token":"wrong_token"
            }   
        }

    def test_google_signup_wrong_token_failure(self):
        request = self.factory.post('api/users/googleauth/', data = json.dumps(self.google_wrong_token_body), content_type = "application/json")
        response = GoogleLoginAPIView.as_view()(request)
        self.assertEqual(response.data['errors']['googleauth_token'][0], "Your google token is not valid!")
        self.assertEqual(response.status_code, 400)

    def test_facebook_signup_no_token_failure(self):
        request = self.factory.post('api/users/googleauth/', content_type = "application/json")
        response = GoogleLoginAPIView.as_view()(request)
        self.assertEqual(response.data['errors']['googleauth_token'][0], "This field is required.")
        self.assertEqual(response.status_code, 400)
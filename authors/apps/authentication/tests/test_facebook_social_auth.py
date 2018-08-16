from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import FacebookLoginAPIView
from authors.apps.authentication.models import User
import json
import urllib.request


class FacebookLoginTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.fb_wrong_token_body = {
            "user":{
                "fbauth_token":"wrong_token"
            }   
        }
    
    def test_facebook_signup_success(self):
        request_test_data = urllib.request.urlopen('https://graph.facebook.com/236382123651778/accounts/test-users?access_token=236382123651778|ea55d9e893e2d05e5a6651d9d37ce85b')
        test_user = json.loads(request_test_data.read())

        fb_token_body = {
            "user":{
                "fbauth_token":test_user["data"][0]["access_token"]
            }   
        }
        request = self.factory.post('api/users/fbauth/', data = json.dumps(fb_token_body), content_type = "application/json")
        response = FacebookLoginAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
        users_queryset = User.objects.filter(username = 'Open Graph Test User')
        self.assertEqual(len(users_queryset), 1)
        self.assertEqual(users_queryset[0].email, 'open_xntkqrw_user@tfbnw.net')

    def test_facebook_signup_wrong_token_failure(self):
        request = self.factory.post('api/users/fbauth/', data = json.dumps(self.fb_wrong_token_body), content_type = "application/json")
        response = FacebookLoginAPIView.as_view()(request)
        self.assertEqual(response.data['errors']['fbauth_token'][0], "The Facebook token provided is not valid!")
        self.assertEqual(response.status_code, 400)

    def test_facebook_signup_no_token_failure(self):
        request = self.factory.post('api/users/fbauth/', content_type = "application/json")
        response = FacebookLoginAPIView.as_view()(request)
        self.assertEqual(response.data['errors']['fbauth_token'][0], "This field is required.")
        self.assertEqual(response.status_code, 400)








        



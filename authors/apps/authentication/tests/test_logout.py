from django.test import TestCase,RequestFactory
from authors.apps.profiles.views import ProfileView,UserUpdate
from authors.apps.authentication.models import User
from authors.apps.authentication.views import LoginAPIView,LogoutAPIView
import json

class LogoutTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='rutale',
            email='rutale@gmail.com',
            password='rutale1234*'
        )
        self.user.is_verified = True
        self.user.save()
        self.user_to_register = {
            "user":{
                 "email": "rutale@gmail.com",
                 "password": "rutale1234*",
                  "username":"rutale"
            }
        }
        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.make_token(self.user_to_register)
        }

    def make_token(self, user):
        request = self.factory.post(
            '/api/users/login/', data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        return response.data['token']
        
    def test_logout_normal(self):
        request=self.factory.post(
            '/api/users/logout/',**self.headers)
        response = LogoutAPIView.as_view()(request)
        self.assertIn('User has been logged out.',response.data["message"])
        self.assertEqual(response.status_code,200)

    def test_logout_already_logged_out(self):
        request=self.factory.post(
            '/api/users/logout/',**self.headers)
        response = LogoutAPIView.as_view()(request)
        response = LogoutAPIView.as_view()(request)
        self.assertIn('User is logged out. Please log in and try again!',response.data["detail"])
        self.assertEqual(response.status_code,403)

    def test_logout_missing_token(self):
        request=self.factory.post(
            '/api/users/logout/')
        response = LogoutAPIView.as_view()(request)
        self.assertIn('Authentication credentials were not provided.',response.data["detail"])
        self.assertEqual(response.status_code,403)
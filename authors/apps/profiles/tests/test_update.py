from django.test import TestCase,RequestFactory
from authors.apps.profiles.views import ProfileView,UserUpdate
from authors.apps.authentication.models import User
from authors.apps.authentication.views import LoginAPIView
from PIL import Image
import json
import tempfile

class UpdateTestCase(TestCase):
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

    def test_update_bio_normal(self):
        user_update = {
                'email': 'rutale@gmail.com',
                'bio': 'rutalez new bio'
            }
        request=self.factory.put(
            "/api/profiles/update/", **self.headers, data=json.dumps(user_update), content_type='application/json')
        response = UserUpdate.as_view()(request)
        self.assertIn('rutalez new bio',response.data["bio"])
        self.assertEqual(response.status_code,200)

    def test_update_bio_missing_email(self):
        user_update = {
                'email': '',
                'bio': 'rutalez new bio'
            }
        request=self.factory.put(
            "/api/profiles/update/",**self.headers, data=json.dumps(user_update), content_type='application/json')

        response = UserUpdate.as_view()(request)
        self.assertIn('One of the input fields is empty.',response.data["error"])
        self.assertEqual(response.status_code,400)

    def test_update_username_normal(self):
        user_update = {
                'email': 'rutale@gmail.com',
                'username': 'rutalez'
            }
        request=self.factory.put(
            "/api/profiles/update/",**self.headers, data=json.dumps(user_update), content_type='application/json')
        response = UserUpdate.as_view()(request)
        self.assertIn('rutalez',response.data["username"])
        self.assertEqual(response.status_code,200)

    def test_update_username_empty_username(self):
        user_update = {
                'email': 'rutale@gmail.com',
                'username': ''
            }
        request=self.factory.put(
            "/api/profiles/update/",**self.headers, data=json.dumps(user_update), content_type='application/json')
        response = UserUpdate.as_view()(request)
        self.assertIn('One of the input fields is empty.',response.data["error"])
        self.assertEqual(response.status_code,400)

    
        
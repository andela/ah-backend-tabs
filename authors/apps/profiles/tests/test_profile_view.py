from django.test import TestCase,RequestFactory
from authors.apps.profiles.views import ProfileView,UserUpdate
from authors.apps.authentication.models import User
from authors.apps.authentication.views import RegistrationAPIView
import json

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # self.user = User.objects.create_user(
        #     username='rutale',
        #     email='rutale@gmail.com',
        #     password='pass'
        # )
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
            '/api/users/', data=json.dumps(user), content_type='application/json')
        response = RegistrationAPIView.as_view()(request)
        return response.data['token']
        
    def test_get_profile_normal(self):
        request=self.factory.get(
            "/api/profiles?id={}".format(
                User.objects.filter(email=self.user_to_register["user"]["email"])[0].id
                ),**self.headers)
        response = ProfileView.as_view()(request)
        self.assertIn('rutale',response.data["username"])
        self.assertEqual(response.status_code,200)

    def test_get_profile_missing_id(self):
        request=self.factory.get(
            "/api/profiles",**self.headers)
        response = ProfileView.as_view()(request)
        self.assertIn('The id was not supplied by the requesting url.',response.data["error"])
        self.assertEqual(response.status_code,400)

    def test_get_profile_non_existing_id(self):
        request=self.factory.get(
            "/api/profiles/?id=300",**self.headers)
        response = ProfileView.as_view()(request)
        self.assertIn('This user id does not exist.',response.data["error"])
        self.assertEqual(response.status_code,400)

    

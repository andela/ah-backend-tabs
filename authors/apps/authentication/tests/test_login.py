from django.test import TestCase,RequestFactory
from authors.apps.authentication.views import LoginAPIView,RegistrationAPIView
import json

class LoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_to_login = {
            'user': {
                'username': 'rutale',
                'email': 'rutale@gmail.com',
                'password': 'rutaleivan#'
            }
        }
        request = self.factory.post(
            "/api/users/", data=json.dumps(self.user_to_login), content_type='application/json')
        RegistrationAPIView.as_view()(request)

    def test_normal_login(self):
        request=self.factory.post(
            "/api/users/login", data=json.dumps(self.user_to_login), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertEqual(response.status_code,200)

    def test_login_wrong_email(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
                'password': 'rutaleivan#'
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('A user with this email and password was not found.',response.data["errors"]["error"][0])
        self.assertEqual(response.status_code,400)

    def test_login_wrong_password(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rutale@gmail.com',
                'password': 'rutale'
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertEqual(response.status_code,400)

    def test_login_missing_email(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': '',
                'password': 'rutaleivan#'
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field may not be blank.',response.data["errors"]["email"][0])
        self.assertEqual(response.status_code,400)

    def test_login_missing_password(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
                'password': ''
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field may not be blank.',response.data["errors"]["password"][0])
        self.assertEqual(response.status_code,400)

    def test_datastructure_user_error_missing_email_index(self):
        user = {
            'user': {
                'username': 'rutale',
                '': 'rut@gmail.com',
                'password': ''
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',response.data["errors"]["email"][0])
        self.assertEqual(response.status_code,400)

    def test_datastructure_user_error_missing_password_index(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
                '': 'rutaleivan'
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',response.data["errors"]["password"][0])
        self.assertEqual(response.status_code,400)

    def test_datastructure_user_error_missing_password_field(self):
        user = {
            'user': {
                'username': 'rutale',
                'email': 'rut@gmail.com',
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',response.data["errors"]["password"][0])
        self.assertEqual(response.status_code,400)

    def test_datastructure_user_error_missing_email_field(self):
        user = {
            'user': {
                'username': 'rutale',
                'password': 'rutaleivan#'
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)
        self.assertIn('This field is required.',response.data["errors"]["email"][0])
        self.assertEqual(response.status_code,400)

    def test_datastructure_user_error_missing_username_field(self):
        user = {
            'user': {
                'email': 'rutale@gmail.com',
                'password': 'rutaleivan#'
            }
        }
        request=self.factory.post(
            "/api/users/login", data=json.dumps(user), content_type='application/json')
        response = LoginAPIView.as_view()(request)

        self.assertEqual(response.status_code,200)

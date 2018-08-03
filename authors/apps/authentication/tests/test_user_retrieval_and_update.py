from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import UserRetrieveUpdateAPIView
from authors.apps.authentication.models import User, UserManager


class UserUpdateRetrievalTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.manager = User.objects
        self.user = self.manager.create_user(
            'username', 'email@gmail.com', 'password')

    def test_no_auth_headers(self):
        """tests whether authentiction has headers """
        request = self.factory.get('api/user/')
        response = UserRetrieveUpdateAPIView.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_user_create_without_password_success(self):
        """tests whether user is created successfully without password"""
        user = self.manager.create_user(
            username='username2', email='email2@gmail.com', password=None)
        self.assertEqual(user.email, 'email2@gmail.com')

    def test_create_user_fail_no_email(self):
        """raise the appropriate exception when an email is missing"""
        with self.assertRaises(Exception) as context:
            self.manager.create_user(
                username='useranme', email=None, password='password')
        self.assertTrue(
            'Users must have an email address.' in str(context.exception))

    def test_create_user_fail_no_username(self):
        """raise the appropriate exception when a username is missing"""
        with self.assertRaises(Exception) as context:
            self.manager.create_user(
                username=None, email='user@gmail.com', password='password')
        self.assertTrue(
            'Users must have a username.' in str(context.exception))        

    def test_create_super_user_fail_no_password(self):
        """raise the appropriate exception when super user password is missing"""
        with self.assertRaises(Exception) as context:
            self.manager.create_superuser(
                username='superuser', email='superuser@gmail.com', password=None)
        self.assertTrue(
            'Superusers must have a password.' in str(context.exception))

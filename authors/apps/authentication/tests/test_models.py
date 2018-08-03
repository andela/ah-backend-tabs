from django.test import TestCase, RequestFactory
from authors.apps.authentication.models import User, UserManager


class ModelsTestcase(TestCase):
    def setUp(self):
        self.manager = User.objects
        self.user = self.manager

    def test_create_user_fail_no_username(self):
        """raise the appropriate exception when an username is missing"""
        with self.assertRaises(Exception) as context:
            self.user.create_user(
                username='', email='user@gmail.com', password='userpassword#777')
        self.assertRaises(
            TypeError, 'Users must have a username.' in str(context.exception))

    def test_create_user_fail_no_email(self):
        """raise the appropriate exception when an email is missing"""
        with self.assertRaises(Exception) as context:
            self.user.create_user(
                username='ronzalo_castro', email='', password='userpassword#777')
        self.assertRaises(
            TypeError, 'Users must have an email address.' in str(context.exception))

    def test_create_superuser_fail_no_password(self):
        """raise the appropriate exception when an password for superuser is missing"""
        with self.assertRaises(Exception) as context:
            self.user.create_superuser(
                username='superuser_rocks', email='superuser@gmail.com', password='')
        self.assertRaises(
            TypeError, 'Superusers must have a password.' in str(context.exception))

    def test_create_user_success(self):
        """tests whether user is created successfully"""
        user = self.user.create_user(
            username='ronzalo_castro', email='ronzalo_castro@gmail.com', password='userpassword#777')
        self.assertEqual(user.email, 'ronzalo_castro@gmail.com')
        self.assertEqual(user.get_full_name, 'ronzalo_castro')
        self.assertEqual(user.get_short_name, 'ronzalo_castro')

    def test_create_super_user_success(self):
        """tests whether super user is created successfully"""
        super_user = self.user.create_superuser(
            username='superuser_rocks', email='superuser@gmail.com', password='superuserpassword#777')
        self.assertEqual(super_user.email, 'superuser@gmail.com')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertEqual(super_user.get_full_name, 'superuser_rocks')
        self.assertEqual(super_user.get_short_name, 'superuser_rocks')

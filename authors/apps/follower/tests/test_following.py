from django.test import TestCase, RequestFactory
from authors.apps.authentication.views import RegistrationAPIView, VerificationAPIView
from authors.apps.follower.views import FollowAPIView, UnfollowAPIView, ListFollowers, ListFollowing
import json
import smtplib
from minimock import Mock
from authors.apps.follower.models import Connect
from authors.apps.authentication.models import User
from django.shortcuts import get_object_or_404


class UserFollowingTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }

        self.user_two = {
            "user": {
                "email": "test2@gmail.com",
                "username": "tester2",
                "password": "testpass@word"
            }
        }
        smtplib.SMTP = Mock('smtplib.SMTP', tracker=None)
        smtplib.SMTP.mock_returns = Mock('smtp_connection')
   
        self.request = self.factory.post(
            '/api/users/', data=json.dumps(self.user), content_type='application/json')
        self.response = RegistrationAPIView.as_view()(self.request)

        self.request_two = self.factory.post(
            '/api/users/', data=json.dumps(self.user_two), content_type='application/json')
        self.response_two = RegistrationAPIView.as_view()(self.request_two)

        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response.data["token"]
        }

        self.headers_two = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response_two.data["token"]
        }

        verfication_request = self.factory.put('/api/users/verify/token',content_type='application/json')
        VerificationAPIView.as_view()(verfication_request, **{"token":self.response.data["token"]})

        verfication_request_two = self.factory.put('/api/users/verify/token',content_type='application/json')
        VerificationAPIView.as_view()(verfication_request_two, **{"token":self.response_two.data["token"]})

    def test_user_follow_success(self):
        request_follow = self.factory.post('/api/users/tester2/follow/', **self.headers, content_type = 'application/json')
        response_follow = FollowAPIView().as_view()(request_follow, **{"username":"tester2"})
        self.assertEqual(response_follow.data["message"], "You are following tester2!")
        self.assertEqual(response_follow.status_code, 200)

        request_follow_back = self.factory.post('/api/users/tester/follow/', **self.headers_two, content_type = 'application/json')
        response_follow_back = FollowAPIView().as_view()(request_follow_back, **{"username":"tester"})
        self.assertEqual(response_follow_back.data["message"], "You are following tester!")
        self.assertEqual(response_follow_back.status_code, 200)

    def test_user_follow_fail_unauthenticated(self):
        request_follow = self.factory.post('/api/users/tester2/follow/',content_type = 'application/json')
        response_follow = FollowAPIView().as_view()(request_follow, **{"username":"tester2"})
        self.assertEqual(response_follow.data["detail"], "Authentication credentials were not provided.")
        self.assertEqual(response_follow.status_code, 403)


    def test_user_unfollow_success(self):
        request_follow = self.factory.post('/api/users/tester2/follow/', **self.headers, content_type = 'application/json')
        response_follow = FollowAPIView().as_view()(request_follow, **{"username":"tester2"})
        self.assertEqual(response_follow.status_code, 200)

        request = self.factory.delete('/api/users/tester2/unfollow/', **self.headers, content_type = 'application/json')
        response = UnfollowAPIView().as_view()(request, **{"username":"tester2"})
        self.assertEqual(response.data["message"],"You unfollowed tester2!")
        self.assertEqual(response.status_code, 200)

    def test_no_duplicate_follows(self):
        request_follow = self.factory.post('/api/users/tester2/follow/', **self.headers, content_type = 'application/json')
        response_follow = FollowAPIView().as_view()(request_follow, **{"username":"tester2"})
        self.assertEqual(response_follow.status_code, 200)

        request_follow_two = self.factory.post('/api/users/tester2/follow/', **self.headers, content_type = 'application/json')
        response_follow_two = FollowAPIView().as_view()(request_follow_two, **{"username":"tester2"})
        self.assertEqual(response_follow_two.data["message"], "You already followed this user!")
        self.assertEqual(response_follow_two.status_code, 403)

        connections = Connect.objects.all()

        self.assertEqual(connections[0].__str__(), "tester is following tester2")
        self.assertEqual(len(connections), 1)

    def test_no_duplicate_unfollow_actions(self):
        request_follow = self.factory.post('/api/users/tester2/follow/', **self.headers, content_type = 'application/json')
        response_follow = FollowAPIView().as_view()(request_follow, **{"username":"tester2"})
        self.assertEqual(response_follow.status_code, 200)

        request_unfollow = self.factory.delete('/api/users/tester2/unfollow/', **self.headers, content_type = 'application/json')
        response_unfollow = UnfollowAPIView().as_view()(request_unfollow, **{"username":"tester2"})
        self.assertEqual(response_unfollow.status_code, 200)

        request_unfollow_two = self.factory.delete('/api/users/tester2/unfollow/', **self.headers, content_type = 'application/json')
        response_unfollow_two = UnfollowAPIView().as_view()(request_unfollow_two, **{"username":"tester2"})
        self.assertEqual(response_unfollow_two.data["message"],"You are not following this user!")
        self.assertEqual(response_unfollow_two.status_code, 403)

        connections = Connect.objects.all()

        self.assertEqual(len(connections), 0)

    def test_list_followers(self):
        request_follow = self.factory.post('/api/users/tester2/follow/', **self.headers, content_type = 'application/json')
        response_follow = FollowAPIView().as_view()(request_follow, **{"username":"tester2"})
        self.assertEqual(response_follow.status_code, 200)


        user_two = get_object_or_404(User, username = "tester2")
        user_two_followers = user_two.followers.all()
        print(user_two_followers)
        self.assertEqual(user_two_followers[0].username, "tester")

        request_get_followers = self.factory.get('api/users/my/followers', **self.headers_two, content_type = 'application/json')
        response_get_followers = ListFollowers.as_view()(request_get_followers)
        self.assertEqual(response_get_followers.data["count"], 1)
        self.assertEqual(response_get_followers.data["results"][0]["username"], "tester")
        self.assertEqual(response_get_followers.status_code, 200)

    def test_list_following(self):
        request_follow = self.factory.post('/api/users/tester2/follow/', **self.headers, content_type = 'application/json')
        response_follow = FollowAPIView().as_view()(request_follow, **{"username":"tester2"})
        self.assertEqual(response_follow.status_code, 200)


        user = get_object_or_404(User, username = "tester")
        user_following = user.following.all()
        self.assertEqual(user_following[0].username, "tester2")

        request_get_following = self.factory.get('api/users/my/following', **self.headers, content_type = 'application/json')
        response_get_following = ListFollowing.as_view()(request_get_following)
        self.assertEqual(response_get_following.data["count"], 1)
        self.assertEqual(response_get_following.data["results"][0]["username"], "tester2")
        self.assertEqual(response_get_following.status_code, 200)
   

    
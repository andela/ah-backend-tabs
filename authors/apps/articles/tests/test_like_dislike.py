from django.test import TestCase, RequestFactory
from authors.apps.articles.views import ArticleCreateAPIView,LikeArticleAPIView,DislikeArticleAPIView
from authors.apps.authentication.views import LoginAPIView
from rest_framework.test import force_authenticate
from authors.apps.authentication.models import User
import json

class LikeDislikeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user" : {
            "email":"test@gmail.com",
            "username":"tester",
            "password":"testpass@word"
        }
        }

        user = User.objects.create_user(self.user["user"]["username"], self.user["user"]["email"], self.user["user"]["password"])
        user.is_verified = True
        user.save()

        self.article_data = {
                "title":"How to Survive",
                "description":"How?",
                "body":"This is how to survive"
            }

        self.request = self.factory.post('/api/users/login/', data = json.dumps(self.user), content_type='application/json')
        self.response = LoginAPIView.as_view()(self.request)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response.data["token"]
        }
        

        request = self.factory.post('api/articles', data = json.dumps(self.article_data), **self.headers, content_type = 'application/json')
        response = ArticleCreateAPIView.as_view()(request)

    def test_like_normal(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/like', **self.headers)
        response = LikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 201)

    def test_like_already_liked(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/like', **self.headers)
        response = LikeArticleAPIView.as_view()(request,**kwargs)
        response = LikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 409)
   
    def test_like_missing_slug(self):
        request = self.factory.post('api/articles/like', **self.headers)
        response = LikeArticleAPIView.as_view()(request)        
        self.assertEqual(response.status_code, 404)

    def test_delete_like_normal(self):
        kwargs = {"slug":"how-to-survive"}
        LikeArticleAPIView.as_view()(self.factory.post('api/articles/how-to-survive/like', **self.headers),**kwargs)
        request = self.factory.delete('api/articles/how-to-survive/like', **self.headers)
        response = LikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_delete_like_before_like(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.delete('api/articles/how-to-survive/like', **self.headers)
        response = LikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 409)

    def test_delete_like_missing_slug(self):
        request = self.factory.delete('api/articles/like', **self.headers)
        response = LikeArticleAPIView.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_dislike_normal(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/dislike', **self.headers)
        response = DislikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 201)

    def test_dislike_already_disliked(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/dislike', **self.headers)
        response = DislikeArticleAPIView.as_view()(request,**kwargs)
        response = DislikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 409)

    def test_dislike_missing_slug(self):
        request = self.factory.post('api/articles/dislike', **self.headers)
        response = DislikeArticleAPIView.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def test_delete_dislike_normal(self):
        kwargs = {"slug":"how-to-survive"}
        DislikeArticleAPIView.as_view()(self.factory.post('api/articles/how-to-survive/dislike', **self.headers),**kwargs)
        request = self.factory.delete('api/articles/how-to-survive/dislike', **self.headers)
        response = DislikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_delete_dislike_before_dislike(self):
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.delete('api/articles/how-to-survive/dislike', **self.headers)
        response = DislikeArticleAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 409)

    def test_delete_dislike_missing_slug(self):
        request = self.factory.delete('api/articles//dislike', **self.headers)
        response = DislikeArticleAPIView.as_view()(request,)
        self.assertEqual(response.status_code, 404)

    

    

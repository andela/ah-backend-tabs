from django.test import TestCase, RequestFactory
from authors.apps.articles.views import CommentCreateAPIView,ArticleCreateAPIView
from authors.apps.authentication.views import RegistrationAPIView
from rest_framework.test import force_authenticate
import json

class CreateCommentTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = {
            "user" : {
            "email":"test@gmail.com",
            "username":"tester",
            "password":"testpass@word"
        }
        }

        self.request = self.factory.post('/api/users/', data = json.dumps(self.user), content_type='application/json')
        self.response = RegistrationAPIView.as_view()(self.request)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.response.data["token"]
        }

        self.article_data = {
                "title":"How to Survive",
                "description":"How?",
                "body":"This is how to survive"
            }


        request = self.factory.post('api/articles', data = json.dumps(self.article_data), **self.headers, content_type = 'application/json')
        response = ArticleCreateAPIView.as_view()(request)

    def test_comment_created_successful(self):
        comment = {
	    "body":"This is a comment"
        }
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/comment', data = json.dumps(comment), **self.headers, content_type = 'application/json')
        response = CommentCreateAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 201)

    def test_comment_empty_body(self):
        comment = {
	    "body":""
        }
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/comment', data = json.dumps(comment), **self.headers, content_type = 'application/json')
        response = CommentCreateAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 400)

    def test_comment_missing_field(self):
        comment = {
	    
        }
        kwargs = {"slug":"how-to-survive"}
        request = self.factory.post('api/articles/how-to-survive/comment', data = json.dumps(comment), **self.headers, content_type = 'application/json')
        response = CommentCreateAPIView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 400)

    def test_comment_url_missing_slug(self):
        comment = {
	    "body":"This is a comment"
        }
        
        request = self.factory.post('api/articles/comment', data = json.dumps(comment), **self.headers, content_type = 'application/json')
        response = CommentCreateAPIView.as_view()(request)
        self.assertEqual(response.status_code, 404)


   
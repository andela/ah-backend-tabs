from django.test import TestCase, RequestFactory
from authors.apps.articles.views import ListAllArticlesAPIView, ArticleCreateAPIView
from authors.apps.authentication.views import RegistrationAPIView, VerificationAPIView


class FetchAllArticlesTestCase(TestCase):
    def setUp(self):

        self.user = {
            "user": {
                "email": "test@gmail.com",
                "username": "tester",
                "password": "testpass@word"
            }
        }

        self.obj = UtilClass()
        registered_user = self.obj.get_reg_data(self.user)
        self.obj.verify_user({"token": registered_user.data["token"]})
        logged_in_user = self.obj.get_login_data(self.user)

        self.headers = {
            'HTTP_AUTHORIZATION': 'Token ' + logged_in_user.data["token"]
        }

        def test_fetch_all_existing_articles(self):
            article_data = {
                "title": "This is Postman",
                "description": "Hello Postman",
                "body": "Hahahaha",
                "tags": ["post", "man"]
            }

            make_article_request = self.factory.post('api/articles', data=json.dumps(
                article_data), **self.headers, content_type='application/json')

            ArticleCreateAPIView.as_view()(make_article_request)

            request = self.factory.get('api/all/articles/')
            response = ListAllArticlesAPIView.as_view()(request)
            self.assertEqual(response.data['results'][count], 1)
            self.assertEqual(
                response.data['results']['articles'][0]['title'], "This is Postman")

        def test_fetch_all_from_empty_db(self):
            request = self.factory.get('api/all/articles/')
            response = ListAllArticlesAPIView.as_view()(request)
            self.assertEqual(response.data['results'][count], 0)
            self.assertEqual(
                len(response.data['results']['articles']), 0)

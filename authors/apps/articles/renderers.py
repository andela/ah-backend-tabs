import json

from rest_framework.renderers import JSONRenderer

from django.urls import reverse_lazy



class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            'article': data,
        })

class ListArticlesJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if "results" in data:
            data["articles"] = data.pop("results")

        return json.dumps({
            "results":data,
        })

class RateArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            'rating': data,
        })

class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            'comment': data,
        })
    

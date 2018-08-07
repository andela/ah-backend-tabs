import json

from rest_framework.renderers import JSONRenderer

from django.urls import reverse_lazy



class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            'article': data,
        })

class RateArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            'rating': data,
        })

import facebook
from rest_framework import serializers

class FacebookValidation:

    @staticmethod
    def validate_facebook_token(auth_token):

        try:

            graph = facebook.GraphAPI(access_token = auth_token, version = "2.7")

            profile = graph.request('/me?fields=id,name,email,picture')

            return profile

        except:

            raise serializers.ValidationError("The Facebook token provided is not valid!")

from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import serializers
import os

class GoogleValidation:

    @staticmethod
    def validate_google_token(google_token):

        CLIENT_ID = os.getenv('CLIENT_ID')

        try:
            idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), CLIENT_ID)

            return idinfo


        except:
            raise serializers.ValidationError("Your google token is not valid!")


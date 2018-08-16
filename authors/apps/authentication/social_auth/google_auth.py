from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import serializers
import os

class GoogleValidation:

    @staticmethod
    def validate_google_token(google_token):

        CLIENT_ID = "341988301600-odl0nb10vaim96gsdhpa6vun7iog5pl0.apps.googleusercontent.com"

        try:
            idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), CLIENT_ID)

            return idinfo


        except:
            raise serializers.ValidationError("Your google token is not valid!")


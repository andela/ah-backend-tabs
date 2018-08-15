from django.urls import path

from .views import (
    LoginAPIView,
    LogoutAPIView, 
    RegistrationAPIView, 
    UserRetrieveUpdateAPIView, 
    VerificationAPIView, 
    SendPasswordResetEmailAPIView, 
    ResetPasswordAPIView,
    FacebookLoginAPIView,
    GoogleLoginAPIView,
)

app_name = "authentication"

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/logout/', LogoutAPIView.as_view()),
    path('users/verify/<token>', VerificationAPIView.as_view(), name='verification'),
    path('users/password/forgot/',
         SendPasswordResetEmailAPIView.as_view(), name='forgot_password'),
    path('users/password/reset/<token>',
         ResetPasswordAPIView.as_view(), name='reset_password'),

    path('users/fbauth/', FacebookLoginAPIView.as_view()),
    path('users/googleauth/', GoogleLoginAPIView.as_view()),
]


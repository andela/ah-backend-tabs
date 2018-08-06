from django.urls import path

from .views import (
   UserUpdate,ProfileView
)

app_name = "profiles"

urlpatterns = [
    path('', ProfileView.as_view()),
    path('update/', UserUpdate.as_view()),
]

from django.urls import path
from .views import FollowAPIView, UnfollowAPIView, ListFollowers, ListFollowing

app_name = "follows"

urlpatterns = [
    path('<username>/follow/', FollowAPIView.as_view()),
    path('<username>/unfollow/',UnfollowAPIView.as_view() ),
    path('my/followers/', ListFollowers.as_view() ),
    path('my/following/', ListFollowing.as_view() ),


]

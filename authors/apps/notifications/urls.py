from django.urls import path

from .views import (
    RetrieveNotifications,
    MarkAsRead,
    OptIn_OptOut_Notifications,
)

app_name = "notifications"

urlpatterns = [
    path('notifications/', RetrieveNotifications.as_view()),
    path('notifications/read/<int:id>', MarkAsRead.as_view()),
    path('notifications/opt_in_or_out', OptIn_OptOut_Notifications.as_view()),
]


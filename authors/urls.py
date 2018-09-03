"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.conf.urls.static import static
from authors.settings.base import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authors.apps.articles.urls')),

    path('api/', include('authors.apps.authentication.urls',
                         namespace='authentication')),
    path('api/profiles/', include('authors.apps.profiles.urls', namespace='profiles')),
    path('api/users/', include('authors.apps.follower.urls', namespace="follows"))
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

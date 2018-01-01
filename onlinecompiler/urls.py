"""onlinecompiler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Ad
    d an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .api import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/login/', login),
    url(r'^api/access_token/', access_token),
    url(r'^api/contest/', contest),
    url(r'^api/usernames/', usernames),
    url(r'^api/register/', register),
    url(r'^api/problem/(?P<problem_code>\w+)', problem),
    url(r'^api/testcases/(?P<problem_code>\w+)', testcases),
    url(r'^api/submit/(?P<problem_code>\w+)', submit),
    url(r'^api/(?P<contest_code>\w+)/', contest_problems),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns + =static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""ifbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import IfBoxHp.views as allview
urlpatterns = [
    path('admin/', admin.site.urls),
    url('top/',allview.newview.as_view()),
    path('', allview.toppage.as_view()),
    path("login",allview.loginview.as_view()),
    path("ifbox", allview.ifboxview.as_view()),
    path("create", allview.createuserview.as_view()),
    path("mypage", allview.mypageview.as_view()),
    path("friends", allview.allfriendview.as_view()),
    path("friendpage", allview.friendpageview.as_view()),
    path("message", allview.sendmessageview.as_view()),
    path("readmail", allview.readmailview.as_view()),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns+=static(settings.IMAGE_URL,document_root=settings.IMAGE_ROOT)

from django.conf.urls import url, include
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^newQuestion$', views.newQuestion, name='newQuestion'),
    url(r'^question/(?P<id>\d+)$', views.question, name='question'),
    url(r'^editQuestion/(?P<id>\d+)$', views.editQuestion, name='editQuestion'),
    url(r'^newAnswer/(?P<id>\d+)$', views.newAnswer, name='newAnswer'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testpost/$', views.testpost, name='testpost'),
    url(r'^createuser', views.createuser, name='createuser'),
    url(r'^loginuser', views.loginuser, name='loginuser'),
    url(r'^logoutuser', views.logoutuser, name='logoutuser'),
    url(r'^deploy', views.deploy, name='deploy')
]

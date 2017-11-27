from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testpost/$', views.testpost, name='testpost'),
    url(r'^createuser', views.createuser, name='createuser'),
    url(r'^loginuser', views.loginuser, name='loginuser'),
    url(r'^logoutuser', views.logoutuser, name='logoutuser'),
    url(r'^createsection', views.createsection, name='createsection'),
    url(r'^sectionsasinstructor', views.sectionsasinstructor, name='sectionsasinstructor'),
    url(r'^enrollinsection', views.enrollinsection, name='enrollinsection'),
    url(r'^sectionsasstudent', views.sectionsasstudent, name='sectionsasstudent'),
    url(r'^createquestion', views.createquestion, name='createquestion'),
    url(r'^answerquestion', views.answerquestion, name='answerquestion'),
    url(r'^getquestionsbysection', views.getquestionsbysection, name='answerquestion'),
    url(r'^getquestiondetail', views.getquestiondetail, name='getquestiondetail'),
    url(r'^deploy', views.deploy, name='deploy')
]

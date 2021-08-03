from django.urls import path

from . import views

app_name = "cognitive_skills" 

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('summary', views.summary, name='summary'),
    path('score', views.score, name='score'),
    path('reset', views.reset, name='reset'),
    path('test/<slug:slug>', views.test, name='test'),
]
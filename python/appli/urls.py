from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'appli'
urlpatterns = [

    path('', views.index, name='index'),

    path('', include('django.contrib.auth.urls')),

    path('project/add', views.addProject, name='addProject'),
    path('project/', views.listProjects, name='listProjects'),

    re_path('project/delete/(?P<projectname>[\w.-]+)', views.deleteProject, name='deleteProject'),

    re_path(r'^project/(?P<projectname>[\w.-]+)/(?P<filename>[\w./-]+)', views.modifyFile, name='modifyFile'),
    re_path('project/(?P<projectname>[\w]+)', views.listBackups, name='detailProject'),
    #path(r'project/(?P<projectname>[\w]+)/backup)', views.listBackups, name='listBackup'),

    

]   

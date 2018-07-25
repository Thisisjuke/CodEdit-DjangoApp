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
    re_path('project/backups/(?P<projectname>[\w.-]+)', views.showBackupsProject, name='showBackupsProject'),
    re_path('project/dobackup/(?P<projectname>[\w.-]+)', views.backupProject, name='backupProject'),
    re_path(r'^project/restorebackup/(?P<projectname>[\w.-]+)/(?P<backupname>[\w.-_]+)', views.restoreBackupProject, name='restoreBackupProject'),
    re_path(r'^project/deletebackup/(?P<projectname>[\w.-]+)/(?P<backupname>[\w.-_]+)', views.deleteBackupProject, name='deleteBackupProject'),

    re_path(r'^project/(?P<projectname>[\w.-]+)/(?P<filename>[\w./-]+)', views.modifyFile, name='modifyFile'),
    re_path('project/(?P<projectname>[\w]+)', views.detailProject, name='detailProject'),

    

]   

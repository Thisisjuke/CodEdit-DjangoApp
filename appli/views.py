from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from .forms import ProjectForm
from .models import Project
import sys,os
import ntpath
from time import gmtime, strftime

# pip install gitpython
import git
from git import Repo
import zipfile

import os
import shutil
import datetime
import time
import sys
import glob
import platform

GLOBAL_DIRSTOCKAGE = os.path.dirname(os.path.normpath(os.path.dirname(os.path.realpath(__file__))))+"\\files"

def index(request):
    if request.user.is_authenticated:
        nb_user = User.objects.count()
        nb_projects = Project.objects.count()
        nb_own = Project.objects.filter(user=request.user).count()
        truc = 0
        context = {'nb_user': nb_user, 'nb_projects': nb_projects, 'nb_own': nb_own, 'truc': truc}
        return render(request, 'appli/index.html', context)

    else:
        return HttpResponseRedirect('login/')
    

def addProject(request):
    if request.user.is_authenticated:

        if request.method == 'POST':

            form = ProjectForm(request.POST)
            if form.is_valid():

                proj = form.save(commit=False)

                extension = ''.join((proj.name).replace(" ", "")).lower()

                pull = pullrepo(proj.link, request.user.username, extension)

                if not pull:
                    
                    proj.user = request.user
                    proj.name = extension
                    proj.save()
                    return HttpResponseRedirect('appli/')
                else: 
                    context = {'message': 'Error : Try with a valid git repository'}
                    return render(request, 'appli/addproject.html', context)

        else:
            form = ProjectForm()
            context = {'form': form}
            return render(request, 'appli/addproject.html', context)

    else:
        return HttpResponseRedirect('login/')

def listProjects(request):
    if request.user.is_authenticated:

        all_projects = Project.objects.filter(user=request.user)
        context = {'all_projects': all_projects}
        return render(request, 'appli/listprojects.html', context)

    else:
        return HttpResponseRedirect('login/')

def detailProject(request, projectname):
    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+request.user.username
    project_path = user_path+"\\"+projectname

    path, dirs, files = next(os.walk(project_path+"_BACKUPS"))
    file_count = len(files) 

    alldir=[]
    
    for path, subdirs, files in os.walk(project_path):
        if not path.split(os.path.sep)[-1] == ".git":
            directory = []
            level = path.replace(project_path, '').count(os.sep)
            directory.append(level)
            directory.append(os.path.basename(os.path.normpath(path)))
            directory.append(path)
            directory.append("folder")
            alldir.append(directory)
            subindent = (level + 1)

            realpath = path.replace('\\','/').split('/'+projectname, 1)[-1]+"/"

            for name in files:
                file = []
                file.append(subindent)
                file.append(name)

                url = realpath + name
                if url.startswith("/"):
                    url = url[1:]

                file.append(url)      
                file.append("file")
                alldir.append(file)
    context = {'alldir': alldir, 'projectname': projectname, 'nb_files':file_count}
    return render(request, 'appli/detailproject.html', context)

def showBackupsProject(request, projectname):
    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+request.user.username
    project_path = user_path+"\\"+projectname+"_BACKUPS"

    alldir=[]
    if os.path.isdir(project_path):
        os.chdir(project_path)
        for file in glob.glob("*.zip"):
            c = strftime("%d-%m-%Y %H:%M", gmtime(float(creation_date(file))))
            alldir.append((file, c))
    context = {'alldir': alldir, 'projectname': projectname}
    return render(request, 'appli/listBackup.html', context)

def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

def modifyFile(request,projectname,filename):

    if request.user.is_authenticated:

        type = os.path.splitext(filename)[1][1:]
        switcher = {
            "html": "htmlmixed",
            "css": "css",
            "py": "python",
            "php": "php",
            "sql": "sql",
            "py": "python",
            "js": "javascript",
            "xml": "xml",
            "json": "javascript",
        }
        extension = switcher.get(type, "none")

        if request.POST.get("content", ""):

            content = '\n'.join([x for x in request.POST.get("content", "").splitlines() if x.strip()])

            setfile(request.user.username, projectname, filename, content)

        content = getfile(request.user.username, projectname, filename)
        
        context = {
            'projectname': projectname,
            'filename': filename,
            'extension': extension,
            'content': content
        }
        return render(request, 'appli/modifyFile.html', context)

def deleteProject(request, projectname):
    project = get_object_or_404(Project, name=projectname, user=request.user)
    deleterepo(request.user.username, projectname)
    Project.objects.filter(name=projectname).delete()
    return HttpResponseRedirect('/appli/project/')

def backupProject(request, projectname):
    project = get_object_or_404(Project, name=projectname, user=request.user)
    dobackup(request.user.username,projectname)
    return HttpResponseRedirect('/appli/project/'+projectname)

def restoreBackupProject(request, projectname, backupname):
    restorebackup(request.user.username, projectname, backupname)
    return HttpResponseRedirect('/appli/project/'+projectname)

def deleteBackupProject(request, projectname, backupname):
    deletebackup(request.user.username, projectname, backupname)
    return HttpResponseRedirect('/appli/project/backups/'+projectname)

#Commandes Python pures, pour la gestion des répertoires. Trouvables dans /functions.py (inutilisé). Coeur de notre projet puis intégrées en Django.
def pullrepo(url, username, projectname):

    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname


    if not os.path.exists(user_path):
        os.makedirs(user_path)

    if not os.path.exists(project_path):
        os.makedirs(project_path)
        os.makedirs(project_path+"_BACKUPS")

    try:
        Repo.clone_from(url, project_path)
    except Exception as e:
        error = 'Error! Type: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e))
        return {'error':error}

def getfile(username, projectname, filename):

    path = GLOBAL_DIRSTOCKAGE.replace('\\','/')
    user_path = path+"/"+username
    project_path = user_path+"/"+projectname
    file_path =  project_path+"/"+filename

    with open(file_path, 'r') as myfile:
        data=myfile.read()
        print(data)
        return data

def setfile(username, projectname, filename, content):

    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname
    file_path =  project_path+"\\"+filename

    with open(file_path, 'w') as myfile:
        myfile.write(content)

def deleterepo(username, projectname):

    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    os.system('rmdir /S /Q "{}"'.format(project_path))
    os.system('rmdir /S /Q "{}"'.format(project_path+"_BACKUPS"))

def dobackup(username,projectname):
    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    zipname = user_path+"\\"+projectname+"_BACKUPS\\"+projectname+"_"+date+'.zip'

    zip_folder(project_path+"\\", zipname)

def zip_folder(folder_path, output_path):
    parent_folder = os.path.dirname(folder_path)
    contents = os.walk(folder_path)

    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:

            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                zip_file.write(absolute_path, relative_path)

            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                zip_file.write(absolute_path, relative_path)
        zip_file.close()
    except zipfile.BadZipfile as message:
        sys.exit(1)


def restorebackup(username,projectname,backupname):
    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname
    backup_path = user_path+"\\"+projectname+"_BACKUPS\\"+backupname

    os.system('rmdir /S /Q "{}"'.format(project_path))
    os.makedirs(project_path)

    z = zipfile.ZipFile(backup_path, 'r')  
    z.extractall(project_path)  
    z.close()

def deletebackup(username,projectname,backupname):
    path = GLOBAL_DIRSTOCKAGE
    user_path = path+"\\"+username
    backup_path = user_path+"\\"+projectname+"_BACKUPS\\"+backupname

    os.remove(backup_path)









"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'appli/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'appli/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'appli/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('appli:results', args=(question.id,)))
"""
# -*- coding: utf-8 -*-
import git
from git import Repo
import zipfile

import os
import shutil
import datetime
import time
import sys

GLOBAL_DIRSTOCKAGE = u'pull'

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
                print "Adding '%s' to archive." % absolute_path
                zip_file.write(absolute_path, relative_path)

    except IOError, message:
        print message
        sys.exit(1)
    except OSError, message:
        print message
        sys.exit(1)
    except zipfile.BadZipfile, message:
        print message
        sys.exit(1)
    finally:
        zip_file.close()

def pullrepo(url, username, projectname):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname


    if not os.path.exists(user_path):
        os.makedirs(user_path)
    else: 
        print('User Already exists')

    if not os.path.exists(project_path):
        os.makedirs(project_path)
        os.makedirs(project_path+"_BACKUPS")

    try:
        Repo.clone_from(url, project_path)
    except Exception as e:
        error = 'Error! Type: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e))
        print(error)

def deleterepo(username, projectname):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    os.system('rmdir /S /Q "{}"'.format(project_path))

def getfile(username, projectname, filename):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname
    file_path =  project_path+"\\"+filename

    with open(file_path, 'r') as myfile:
        data=myfile.read()
        return data

def setfile(username, projectname, filename, content):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname
    file_path =  project_path+"\\"+filename

    with open(file_path, 'w') as myfile:
        myfile.write(content)

def setbranch(username, projectname, branchname):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    repo = Repo(project_path)
    repo.git.checkout('-b', branchname)

def getbranch(username, projectname):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    repo = Repo(project_path)

    branch = repo.active_branch
    return branch.name

def commit(username, projectname, message):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    repo = Repo(project_path)

    try:
        repo.git.add('--all')
        repo.git.commit('-m', message)
    except Exception as e:
        error = 'Error! Type: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e))
        print(error)

def getcommitfeed(username,projectname):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    repo = Repo(project_path)

    master = repo.head.reference
    print master.log()

def gitpush(url, username, projectname):

    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    repo = Repo(project_path)

    branch = getbranch(username, projectname)
    repo.git.push(url, branch)

def dobackup(username,projectname):
    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname

    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    zipname = user_path+"\\"+projectname+"_BACKUPS\\"+projectname+"_"+date+'.zip'

    if not os.path.isfile(zipname):
        zip_folder(project_path+"\\", zipname)

def restorebackup(username,projectname,backupname):
    path = os.path.basename(GLOBAL_DIRSTOCKAGE)
    user_path = path+"\\"+username
    project_path = user_path+"\\"+projectname
    backup_path = user_path+"\\"+projectname+"_BACKUPS\\"+backupname

    deleterepo(username, projectname)
    os.makedirs(project_path)

    z = zipfile.ZipFile(backup_path)  
    z.extractall(project_path)  


'''pullrepo('https://bitbucket.org/jukeboy/fake-datas/src/',"arthur","mytest")'''
'''setfile("arthur","mytest","README.md","NEW LINE \nABRACADABRAA")'''
'''getfile("arthur","mytest","README.md")'''

'''getbranch("arthur","mytest")'''
'''setbranch("arthur","mytest","superbranch")'''
'''getbranch("arthur","mytest")'''

'''commit("arthur","mytest","Init")'''
'''getcommitfeed("arthur","mytest")'''
'''gitpush('https://bitbucket.org/jukeboy/fake-datas/src/','arthur','mytest')'''

'''dobackup("arthur","mytest")'''
'''restorebackup('arthur','mytest','mytest_20180718_190812.zip')'''
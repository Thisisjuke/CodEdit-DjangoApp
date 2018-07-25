# Project Python : CodEdit

## Introduction

> This is the alpha of a web application you can install in your entreprise. With this, each employee can pull his own project, modify it in an application. Usefull for code review.
<u> It's based on Python Django.</u>

## Prerequisites

> You need to install before : 
- Python 3.*
- Django 2.*
- Git 2.*
- GitPython : do ```pip install gitpython```
- NOTICE : At this moment, the application use your own git crendentials. So be sure to pull authorized repository only.*

## Installation

> Once the application downloaded, you will need ton do few commands to migrate the database and create an user.
<br>NOTICE : On windows, add ```python``` before the command like ```python manage.py cmd```

```
# Prepare migrations
manage.py makemigrations

# Do migrations
manage.py migrate 

# Enter informations Django needs to create an user
manage.py createsuperuser 

# Launch Django Server
manage.py runserver 
```
> Now, Go to the URL Django gived you and add /appli, like ```http://127.0.0.1:8000/```

## TO-DO list :

> There are few python functions we want to implement in this Django App in the futur (see functions in /functions.py) :
- Branch Management : setbranch + getbranch 
- Commit Feed of this repo : getcommitfeed
- Pull action : gitpush
- Sign in witout admin command

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Project(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    link = models.CharField(max_length=200) 

    def __str__(self):
        return self.name


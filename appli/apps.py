from django.apps import AppConfig

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.views.generic import TemplateView
from django.conf import settings


class AppliConfig(AppConfig):
    name = 'appli'
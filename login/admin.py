# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

from django.apps import apps

myapp = apps.get_app_config('login')
for model in myapp.get_models():
    admin.site.register(model)
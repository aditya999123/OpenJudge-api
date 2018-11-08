from __future__ import absolute_import
import os
from celery import Celery
from onlinecompiler.settings import BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinecompiler.settings')

app = Celery('celery', broker = BROKER_URL)
# app.config_from_object('django.conf:settings') #, namespace='CELERY')
# app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)

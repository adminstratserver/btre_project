from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btre.settings')
app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
import django
django.setup()
from demoapp.tasks import *

print('running my task')
addtwonumbers.delay(2, 2)

print('running Stratserver')


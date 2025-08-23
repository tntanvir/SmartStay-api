# smarthouse/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarthouse.settings')

app = Celery('smarthouse')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Explicitly register tasks
app.autodiscover_tasks(lambda: ['room', 'reviews', 'booking', 'payment', 'analytics'])


# Optional: Define a debug task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
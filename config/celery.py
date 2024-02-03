from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the environment variable for project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create an instance of a Celery object
app = Celery('config')

# Upload settings from Django file
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# from discusoion skypro
app.conf.broker_connection_retry_on_startup = True

# Automatic detection and registration of tasks from tasks.py files in Django applications
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
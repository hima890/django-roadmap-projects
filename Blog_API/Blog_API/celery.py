import os
from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog_API.settings')

# Create celery app instance
app = Celery('Blog_API')

# Load celery config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Set the autodiscover to True
app.autodiscover_tasks()

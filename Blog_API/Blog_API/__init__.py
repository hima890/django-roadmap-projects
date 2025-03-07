from .celery import app as celery_app

# This '__all__' is used to import the celery_app instance in the __init__.py file of the project
__all__ = ("celery_app",)

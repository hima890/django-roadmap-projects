"""
URL configuration for the API of the simple_task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/

Routes:
- 'overview/': Maps to the `overview` view, provides an overview of tasks.
- 'create_task/': Maps to the `create_task` view, allows creation of a new task.
- 'update_task/': Maps to the `update_task` view, allows updating an existing task.
- 'delete_task/': Maps to the `delete_task` view, allows deletion of a task.
"""
from . import views
from django.urls import path


urlpatterns = [
    path('overview/', views.overview, name='overview'),
    path('create_task/', views.create_task, name='create_task'),
    path('update_task/', views.update_task, name='update_task'),
    path('delete_task/', views.delete_task, name='delete_task'),
]

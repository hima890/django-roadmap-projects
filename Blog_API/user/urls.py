from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.registeView, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update-profile/', views.updateUserProfile, name='updateUserProfile'),
]

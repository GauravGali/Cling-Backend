# Imports
from django.urls import path
from . import views

# Paths
urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('users/', views.getUsers, name='users'),
    path('users/<int:user_id>/', views.getUser, name='user'),
    path('users/create', views.createUser, name='create_user'),
]

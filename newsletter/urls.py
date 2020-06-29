  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('add_subscriber/', views.add_subscriber)
]
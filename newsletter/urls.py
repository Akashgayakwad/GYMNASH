  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'newsletter'

urlpatterns = [
    path('add_subscriber/', views.add_subscriber),
    path('mock/', views.mock),

]
  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'gymowner'

urlpatterns = [
    path('get_gyms_by_city/', views.get_gyms_by_city),
    path('get_gym_details/', views.get_gym_details),
]
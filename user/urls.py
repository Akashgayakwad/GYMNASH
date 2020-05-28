  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('request_otp/', views.request_otp),
    path('verify_otp/', views.verify_otp),
    path('get_profile/',views.get_profile),
    path('update_profile/',views.update_profile),
    path('get_state_list/',views.get_state_list),
    path('get_city_list/',views.get_city_list),
]
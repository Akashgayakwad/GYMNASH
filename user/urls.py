  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('request_otp/', views.request_otp),
    path('verify_otp/', views.verify_otp),
    path('test/',views.test),
    path('update_profile/',views.update_profile),
]
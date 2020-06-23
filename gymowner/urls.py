  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'gymowner'

urlpatterns = [
    path('get_gyms_by_city/', views.get_gyms_by_city),
    path('get_gym_details/', views.get_gym_details),
    path('cred_login/',views.cred_login),
    path('cred_logout/',views.cred_logout),
    path('private_route/',views.private_route),
    path('get_gyms_by_owner/',views.get_gyms_by_owner),
    path('get_all_orders/',views.get_all_orders),
    path('get_new_orders/',views.get_new_orders),
    path('mark_order_as_read/',views.mark_order_as_read),
]
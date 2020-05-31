  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'transaction'

urlpatterns = [
    path('get_monthly_price/',views.get_monthly_price),
    path('create_order/',views.create_order),
    path('verify_payment/',views.verify_payment),
    path('get_expiry/',views.get_expiry)
]
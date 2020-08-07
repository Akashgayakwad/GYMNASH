  
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'transaction'

urlpatterns = [
    path('get_monthly_price/',views.get_monthly_price),
    path('create_order/',views.create_order),
    path('confirm_payment/',views.confirm_payment),
    path('payment_failure/',views.payment_failure),
    path('get_expiry/',views.get_expiry)
]
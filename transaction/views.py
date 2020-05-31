from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from decorators.gym_auth import gym_user 
from decouple import config
from .models import Order
from gymowner.models import GYM

from datetime import datetime,timedelta,date
# Create your views here.


@csrf_exempt
def get_monthly_price(request, *args, **kwargs):
    if request.method == 'POST':
        gym_id = request.POST.get('gym_id')
        try:
            gym = GYM.objects.filter(id=gym_id).first()
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'Some error occured'})
        else:
            if(gym):
                price = gym.price
                return JsonResponse({'status':'success','message':'price fetched successfully','price':price})
            else:
                return JsonResponse(status=404,data={'status':'Failed','message':'GYM id not found'})

@csrf_exempt
def get_expiry(request, *args, **kwargs):
    if request.method == "POST":
        b_id = request.POST.get('b_id')
        try:
            order = Order.objects.filter(booking_id = b_id).first()
        except:
            return JsonResponse(status=500,data={'success':'Failed','message':'Some error occured'})
        else:
            if(order):
                created_at = order.order_timestamp
                expiry  = created_at + timedelta(days = order.months*30)
                print("created_at",created_at)
                print("months",order.months)
                print("expiry",expiry)
                print("now",date.today())
                if(expiry >= date.today()):
                    return JsonResponse({'success':'True','expired':False})
                else:
                    return JsonResponse({'success':'True','expired':True})
                
            else:
                return JsonResponse(status=404,data={'success':'Failed','message':'order with given booking id not found'})


@csrf_exempt
@gym_user
def create_order(request, *args, **kwargs):
    if request.method == 'POST':
        gym_id = request.POST.get('gym_id')
        months = request.POST.get('months')
        try:
            gym = GYM.objects.filter(id = gym_id).first()
        except:
            return JsonResponse(status=404,data={'status':'Failed','message':'gym not found'})
        else:
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'
            notes = {
                'customer_number':request.gymuser.phone,
                'gym_name':gym.gymname,
                'months':months
                }
            order_amount = str(gym.price*int(months)*100)
            try:
                client = razorpay.Client(auth=(config('RZP_KEY'),config('RZP_SECRET')))
                response = client.order.create(dict(amount = order_amount,
                                                currency = order_currency,
                                                receipt = order_receipt,
                                                notes = notes,
                                                payment_capture='0'))
            except:
                return JsonResponse({'status':'Failed','message':'unable to create order at the moment'})
            else:
                order_id = response['id']
                order_status = response['status']
                if(order_status == "created"):
                    order = Order(order_id = order_id, amount = int(order_amount)/100, months = months,gym=gym, user=request.gymuser)
                    order.save()
                    return JsonResponse({'status':'Success','message':'order generated successfully', 'order_id':order_id,'order_status':order_status,'order_amount':order_amount,'order_notes':notes})
                else:
                    return JsonResponse({'status':'Failed','message':'order creation failed by service provider'})



@csrf_exempt
def payment_status(request, *args, **kwargs):
    if request.method == 'POST':
        params_dict = {
            'razorpay_payment_id':request.POST.get('razorpay_payment_id'),
            'razorpay_order_id':request.POST.get('razorpay_order_id'),
            'razorpay_signature':request.POST.get('razorpay_signature'),
        }
        try:
            client = razorpay.Client(auth=(config('RZP_KEY'),config('RZP_SECRET')))
            status = client.utility.verify_payment_signature(params_dict)
        except:
            return JsonResponse({'status':'Payment Failed'})
        else:
            return JsonResponse({'status':'Payment Successful'})

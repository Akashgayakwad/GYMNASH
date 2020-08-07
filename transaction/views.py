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

def my_bool(mystr):
    if mystr == "True":
        return True
    else:
        return False

@csrf_exempt
@gym_user
def create_order(request, *args, **kwargs):
    if request.method == 'POST':
        gym_id = request.POST.get('gym_id')
        count = request.POST.get('count')
        dom = request.POST.get('dom')   #daysormonths
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
                'count':count,
                'dom':dom
                }
            if dom == 'True':
                order_amount = str(gym.daily_price*int(count)*100)
            else:
                order_amount = str(gym.monthly_price*int(count)*100)
            try:
                client = razorpay.Client(auth=(config('RZP_KEY'),config('RZP_SECRET')))
                response = client.order.create(dict(amount = order_amount,
                                                currency = order_currency,
                                                receipt = order_receipt,
                                                notes = notes,
                                                payment_capture='1'))
            except:
                return JsonResponse({'status':'Failed','message':'unable to create order at the moment'})
            else:
                order_id = response['id']
                order_status = response['status']
                if(order_status == "created"):
                    if dom == 'True':
                        expiry  = date.today() + timedelta(days = int(count))
                    else:
                        expiry  = date.today() + timedelta(days = int(count)*30)
                    order = Order(order_id = order_id, amount = int(order_amount)/100, count = count ,dom=my_bool(dom), gym=gym, user=request.gymuser,order_expiry=expiry)
                    order.save()
                    return JsonResponse({'status':'Success','message':'order generated successfully', 'order_id':order_id,'order_status':order_status,'order_amount':order_amount,'order_notes':notes})
                else:
                    return JsonResponse({'status':'Failed','message':'order creation failed by service provider'})



@csrf_exempt
def confirm_payment(request, *args, **kwargs):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')
        payment_signature = request.POST.get('payment_signature')

        params_dict = {
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': payment_signature,
        }

        try:
            client = razorpay.Client(auth=(config('RZP_KEY'),config('RZP_SECRET')))
            status = client.utility.verify_payment_signature(params_dict)
            print(status)
            order = Order.objects.filter(order_id = order_id).first()
            order.payment_id = payment_id
            order.payment_status = "Success"
            order.save()
        except SignatureVerificationError as err:
            return JsonResponse(status=500,data={'status': 'Failed','message':'Payment Verification Failed. Error is'+err})
        else:
            return JsonResponse({'status': 'Success','message':'Payment Verified'})


@csrf_exempt
def payment_failure(request, *args, **kwargs):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')
        payment_err_code = request.POST.get('payment_error_code')
        payment_error_msg = request.POST.get('payment_error_msg')

        try:
            order = Order.objects.filter(order_id = order_id).first()
            order.payment_id = payment_id
            order.payment_status = "Falied"
            order.payment_err_code=payment_err_code
            order.payment_err_msg=payment_err_msg
            order.save()
        except Exception as e:
            return JsonResponse({'status': 'Failed','message':'Payment Status Update Failed','error':str(e)})
        else:
            return JsonResponse({'status': 'Success','message':'Payment Status Updated'})

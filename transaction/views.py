from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay

from decouple import config
from .models import Order
from gymowner.models import GYM
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
def create_order(request, *args, **kwargs):
    if request.method == 'POST':
        client = razorpay.Client(auth=(config('RZP_KEY'),config('RZP_SECRET')))
        order_amount = 100
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping Address': 'Amanaka,Raipur,C.G.'}

        response = client.order.create(dict(amount = order_amount,
                                            currency = order_currency,
                                            receipt = order_receipt,
                                            notes = notes,
                                            payment_capture='0'))
        print(response)
        return JsonResponse({'order_id':response['id'],'order_status':response['status']})


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

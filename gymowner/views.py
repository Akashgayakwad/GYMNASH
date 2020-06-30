from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from decouple import config
import json
import jwt
import random
# from django.shortcuts import get_object_or_none
from datetime import datetime, date, timedelta 
import pytz
from user.models import City
from .models import GYM
from transaction.models import Order
from decorators.gym_auth import cred_user,gym_user
tz = pytz.timezone('Asia/Kolkata')


@csrf_exempt
def cred_login(request, *args, **kwargs):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        try:
            creduser = authenticate(username=username, password=password)
        except ValueError as e:
            print("some error occured while authentication. error msg is : ",str(e))
            return JsonResponse(status=500,data={'status':'Failed','message':'some error occured','error':e})
        else:
            if not creduser:
                return JsonResponse({'status':'Failed','message':'Invalid Login Credentials'})
            else:
                print("user authenticated") 
                payload = {
                'username': creduser.username,
                }
                jwt_token = jwt.encode(payload, config('SECRET_KEY'))
                jwt_token = jwt_token.decode('utf-8')
                return JsonResponse({"status": "Success", "message":"Credentials Matched Successfully","token":jwt_token})


@csrf_exempt
def cred_logout(request):
	logout(request)
	return JsonResponse({'success':True,
						 'message':'User logged out successsfully'})

                         
@csrf_exempt
@cred_user
def private_route(request, *args, **kwargs):
    if request.method == "POST":
        return JsonResponse({'message':'You are authorized','cred_user_username':request.creduser.username,'cred_user_contact':request.creduser.contact})


@csrf_exempt
def get_gyms_by_city(request, *args, **kwargs):
    if request.method=="POST":
        city_name = request.POST.get('city')
        city = City.objects.filter(city=city_name).first()
        if(city):
            try:
                gyms = GYM.objects.filter(city = city)
            except:
                return JsonResponse(status=500,data={"status":"Failed","message":"Some error occured"})
            else:
                print(gyms)
                if gyms.count() <= 0:
                    return JsonResponse(status=404,data={"status":"Failed","message":"No Gyms found for the city"})
                else:
                    gymlist = []
                    for gym in gyms:
                        mygym={}
                        mygym['id'] = gym.id
                        mygym['logo'] = str(gym.logo)
                        mygym['gymname'] = gym.gymname
                        mygym['address'] = gym.address
                        mygym['city'] = str(gym.city)
                        mygym['original_price'] = gym.original_price
                        mygym['daily_price'] = gym.daily_price
                        mygym['monthly_price'] = gym.monthly_price
                        gymlist.append(mygym)
                    return JsonResponse({"status":"Success","message":"Gyms found","gyms":gymlist})
        else:
            return JsonResponse(status=404,data={'status':'Failed','message':'City Not Found'})


@csrf_exempt
@cred_user
def get_gyms_by_owner(request, *args, **kwargs):
    if request.method=="POST":
        try:
            gyms = GYM.objects.filter(gymowner = request.creduser)
        except:
            return JsonResponse(status=500,data={"status":"Failed","message":"Some error occured"})
        else:
            print(gyms)
            if gyms.count() <= 0:
                return JsonResponse(status=404,data={"status":"Failed","message":"No Gyms found for the owner"})
            else:
                gymlist = []
                for gym in gyms:
                    mygym={}
                    mygym['id'] = gym.id
                    mygym['logo'] = str(gym.logo)
                    mygym['gymname'] = gym.gymname
                    mygym['address'] = gym.address
                    mygym['city'] = str(gym.city)
                    mygym['original_price'] = gym.original_price
                    mygym['daily_price'] = gym.daily_price
                    mygym['monthly_price'] = gym.monthly_price
                    gymlist.append(mygym)
                return JsonResponse({"status":"Success","message":"Gyms found","gyms":gymlist})


@csrf_exempt
def get_gym_details(request, *args, **kwargs):
    if request.method=="POST":
        gym_id = request.POST.get('gym_id')
        try:
            gym = GYM.objects.filter(id=gym_id).first()
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'Some error occured'})
        else:
            if(gym):
                mygym={}
                mygym['id'] = gym.id
                mygym['gymname'] = gym.gymname
                mygym['gymowner'] = str(gym.gymowner)
                mygym['feature1'] = gym.feature1
                mygym['feature2'] = gym.feature2
                mygym['feature3'] = gym.feature3
                mygym['feature4'] = gym.feature4
                mygym['feature5'] = gym.feature5
                mygym['gymownercontact'] = str(gym.gymowner.contact)
                mygym['gymowneraadhar'] = str(gym.gymowner.aadhar)
                mygym['address'] = gym.address
                mygym['location'] = gym.location
                mygym['city'] = str(gym.city)
                mygym['original_price'] = gym.original_price
                mygym['daily_price'] = gym.daily_price
                mygym['monthly_price'] = gym.monthly_price
                mygym['logo'] = str(gym.logo)
                mygym['images'] = []
                mygym['images'].append(str(gym.image1))
                mygym['images'].append(str(gym.image2))
                mygym['images'].append(str(gym.image3))
                mygym['images'].append(str(gym.image4))
                mygym['images'].append(str(gym.image5))


                return JsonResponse({"status":"Success","message":"Gym found","gym":mygym})
            else:
                return JsonResponse(status=404,data={'status':'Failed','message':'Gym Not Found'})




@csrf_exempt
@cred_user
def get_all_orders(request, *args, **kwargs):
    if request.method == 'POST':
        gym_id = request.POST.get('gym_id')
        try:
            gym = GYM.objects.filter(id=gym_id, gymowner=request.creduser).first()
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'Some error occured'})
        else:
            if(gym):
                try:
                    orders = Order.objects.filter(payment_status="Success",gym=gym).order_by('-order_timestamp','-booking_id')
                except:
                    return JsonResponse(status=500,data={'status':'Failed','message':'unable to fetch orders at the moment'})
                else:
                    orderlist = []
                    for order in orders:
                        myorder = {}
                        myorder['booking_id']=order.booking_id
                        myorder['customer_name']=str(order.user)
                        myorder['new']=order.new
                        myorder['order_time']=order.order_timestamp
                        myorder['expiry']=order.order_expiry
                        orderlist.append(myorder)
                    return JsonResponse({'status':'Success','message':'All Orders fetched', 'orders':orderlist})

                        
            else:
                return JsonResponse(status=404,data={'status':'Failed','message':'Gym Not Found'})



@csrf_exempt
@cred_user
def get_new_orders(request, *args, **kwargs):
    if request.method == 'POST':
        gym_id = request.POST.get('gym_id')
        try:
            gym = GYM.objects.filter(id=gym_id, gymowner=request.creduser).first()
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'Some error occured'})
        else:
            if(gym):
                try:
                    orders = Order.objects.filter(new=True, payment_status="Success",gym=gym).order_by('-order_timestamp','-booking_id')
                except:
                    return JsonResponse(status=500,data={'status':'Failed','message':'unable to fetch orders at the moment'})
                else:
                    orderlist = []
                    for order in orders:
                        myorder = {}
                        myorder['booking_id']=order.booking_id
                        myorder['customer_name']=str(order.user)
                        myorder['new']=order.new
                        myorder['order_time']=order.order_timestamp
                        myorder['expiry']=order.order_expiry
                        orderlist.append(myorder)
                    return JsonResponse({'status':'Success','message':'All new Orders fetched', 'orders':orderlist})

                        
            else:
                return JsonResponse(status=404,data={'status':'Failed','message':'Gym Not Found'})


@csrf_exempt
@cred_user
def mark_order_as_read(request, *args, **kwargs):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            order = Order.objects.filter(booking_id=booking_id).first()
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'unable to fetch order at the moment'})
        else:
            if(order):
                order.new=False
                order.save()
                return JsonResponse({'status':'Success','message':'Order Successfully marked as read'})
            else:
                return JsonResponse(status=404,data={'status':'Failed','message':'Booking id Not Found'})

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
from decorators.gym_auth import cred_user
tz = pytz.timezone('Asia/Kolkata')


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
                        mygym['price'] = gym.price
                        gymlist.append(mygym)
                    return JsonResponse({"status":"Success","message":"Gyms found","gyms":gymlist})
        else:
            return JsonResponse(status=404,data={'status':'Failed','message':'City Not Found'})

@csrf_exempt
def get_gym_details(request, *args, **kwargs):
    if request.method=="POST":
        id = request.POST.get('gym_id')
        try:
            gym = GYM.objects.filter(id=id).first()
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'Some error occured'})
        else:
            if(gym):
                mygym={}
                mygym['id'] = gym.id
                mygym['gymname'] = gym.gymname
                mygym['gymowner'] = str(gym.gymowner)
                mygym['gymownercontact'] = str(gym.gymowner.contact)
                mygym['gymowneraadhar'] = str(gym.gymowner.aadhar)
                mygym['address'] = gym.address
                mygym['location'] = gym.location
                mygym['city'] = str(gym.city)
                mygym['price'] = gym.price
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
def cred_login(request, *args, **kwargs):
    error_msg = {}
    error_msg['success'] = False
    error_msg['token'] = '' 

    def try_auth(username, password):
        try:
            creduser = authenticate(username=username, password=password)
            if not creduser:
                print('no gym user')
                raise ValueError('Invalid login credentials!')
        except ValueError as e:
            print('caught invalid cred')
            error_msg['message'] = str(e)
        else:
            print('no error')
            error_msg['success'] = True
            error_msg['message'] = "Authentication successful"
            payload = {
                'phone': creduser.contact,
            }
            jwt_token = jwt.encode(payload, config('SECRET_KEY'))
            token = jwt_token.decode('utf-8')
            error_msg['token'] = token
            error_msg['contact'] = creduser.contact
   
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        try_auth(username,password)        
    else:  
        error_msg['message'] = "Bad request"
    return JsonResponse(error_msg)


@csrf_exempt
def cred_logout(request):
	logout(request)
	return JsonResponse({'success':True,
						 'message':'User logged out successsfully'})

                         
# @csrf_exempt
# @cred_user
# def private_route(request, *args, **kwargs):
#     if request.method == "POST":
#         return JsonResponse({'message':'You are authorized','cred_user_contact':request.creduser.contact})
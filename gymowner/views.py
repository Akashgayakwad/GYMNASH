from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import json
import jwt
import random
# from django.shortcuts import get_object_or_none
from datetime import datetime, date, timedelta 
import pytz
from user.models import City
from .models import GYM

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
                        mygym['gymname'] = gym.gymname
                        mygym['address'] = gym.address
                        mygym['city'] = str(gym.city)
                        mygym['price'] = gym.price
                        gymlist.append(mygym)
                    return JsonResponse(status=404,data={"status":"Success","message":"Gyms found","gyms":gymlist})
        else:
            return JsonResponse(status=404,data={'status':'Failed','message':'City Not Found'})

@csrf_exempt
def get_gym_details(request, *args, **kwargs):
    if request.method=="POST":
        id = request.POST.get('gym_id')
        gym = GYM.objects.filter(id=id).first()
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
            mygym['images'] = []
            mygym['images'].append(str(gym.image1))
            mygym['images'].append(str(gym.image2))
            mygym['images'].append(str(gym.image3))
            mygym['images'].append(str(gym.image4))
            mygym['images'].append(str(gym.image5))


            return JsonResponse(status=404,data={"status":"Success","message":"Gym found","gym":mygym})
        else:
            return JsonResponse(status=404,data={'status':'Failed','message':'Gym Not Found'})


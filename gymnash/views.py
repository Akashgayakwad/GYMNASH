from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from decouple import config
# import json
# import jwt
# import random
# # from django.shortcuts import get_object_or_none
# from datetime import datetime, date, timedelta 
# import pytz

from user.models import City,State


@csrf_exempt
def get_state_list(request, *args, **kwargs):
    if request.method=='GET':
        try:
            states = State.objects.all()
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'some error occured'})
        else:
            if(states.count() <= 0):
                return JsonResponse(status=404,data={'status':'Failed','message':'State List not available'})
            statelist = []
            for state in states:
                statelist.append(str(state))
            return JsonResponse({'status':'state list fetched','states':statelist})


@csrf_exempt
def get_city_list(request, *args, **kwargs):
    if request.method=='POST':
        state = request.POST.get('state')
        state = State.objects.filter(state=state).first()
        if(state):
            try:
                cities = City.objects.filter(state=state)
            except:
                return JsonResponse(status=500,data={'status':'Failed','message':'Some error occured'})
            else:
                if(cities.count() <= 0):
                    return JsonResponse(status=404,data={'status':'Failed','message':'No Cities Available'})
                else:
                    citylist = [] 
                    for city in cities:
                        citylist.append(str(city))
                    return JsonResponse({'status':'state list fetched','states':citylist})
        else:
            return JsonResponse(status=404,data={'status':'Failed','message':'State Not Exist'})
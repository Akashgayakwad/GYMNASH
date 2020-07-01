from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import json
import jwt
import random
# from django.shortcuts import get_object_or_none
from datetime import datetime, date, timedelta 
import pytz

from .models import Subscriber

tz = pytz.timezone('Asia/Kolkata')


@csrf_exempt
def add_subscriber(request, *args, **kwargs):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subscriber = Subscriber.objects.create(name=name,email=email)
        try:
            subscriber.save()
        except:
            return JsonResponse(status=500,data={'status': 'Failed', 'message':'Internal Server Error'})
        else:
            return JsonResponse({'status':'Success', 'message':'Newsletter Subscriber added successfully'})

@csrf_exempt
def mock(request,*args,**kwargs):
    return JsonResponse({'sad':'asfasf'})
        
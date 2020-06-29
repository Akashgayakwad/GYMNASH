from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import json
import jwt
import random
# from django.shortcuts import get_object_or_none
from datetime import datetime, date, timedelta 
import pytz

from .models import GymUser,OTP,City,State
from transaction.models import Order
from decorators.gym_auth import gym_user

tz = pytz.timezone('Asia/Kolkata')

@csrf_exempt
def request_otp(request, *args, **kwargs):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        gymuser = GymUser.objects.filter(phone__iexact=phone).first()
        
        if(gymuser):
            pstotp = OTP.objects.filter(user=gymuser).first()
            
            if(pstotp):
                expire_at = pstotp.created_at + timedelta(minutes=1)
                
                if(expire_at <datetime.now()):
                    pin = random.randint(100000, 999999)
                    pstotp.otp=pin
                    pstotp.count=1
                    try:
                        pstotp.save()
                    except:
                        return JsonResponse(status=500, data={'status': 'Failed', 'message':'Unable to generate OTP'})
                    else:
                        print("expired otp replaced with new otp")
                        print("count = ",pstotp.count)
                        return JsonResponse({'status': 'Success', 'message':'New OTP Regenerated','otp':pstotp.otp})
               
                count = pstotp.count
                if(count < 3):
                    pstotp.count=count+1
                    try:
                        pstotp.save()
                    except:
                        return JsonResponse(status=500, data={'status': 'Failed', 'message':'Unable to generate OTP'})
                    else:
                        return JsonResponse({'status': 'Success', 'message':'OTP Already exist','otp':pstotp.otp})
                else:
                    return JsonResponse(status=403, data={'status': 'Failed', 'message':'OTP Limit Exceeded! Contact Customer Service'})

            else:    
                pin = random.randint(100000, 999999)
                otp = OTP(user=gymuser,otp=pin)
                try:
                    otp.save()
                except:
                    return JsonResponse(status=500, data={'status': 'Failed', 'message':'Unable to generate OTP'})
                else:
                    print("count = ",otp.count)
                    return JsonResponse({'status': 'Success', 'message':'OTP generated Successfully','otp':pin})
        
        else:
            gymuser = GymUser.objects.create(phone = phone)
            gymuser.save()
            pin = random.randint(100000, 999999)
            otp = OTP(user=gymuser,otp=pin)
            try:
                otp.save()
            except:
                return JsonResponse(status=500, data={'status': 'Failed', 'message':'Unable to generate OTP'})
            else:
                print("count = ",otp.count)
                return JsonResponse({'status': 'Success', 'message':'OTP Sent Successfully','otp':pin})




@csrf_exempt
def verify_otp(request, *args, **kwargs):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        print("phone",phone)
        print("otp",otp)
        gymuser = GymUser.objects.filter(phone = phone).first()
        if(gymuser):
            sotp = OTP.objects.filter(user = gymuser).first()
            if(sotp):
                expire_at = sotp.created_at + timedelta(minutes = 1)
                print("expire at",expire_at)
                print("date time",datetime.now())
                if(expire_at < datetime.now()):
                        return JsonResponse({"status":"Failed","Message":"OTP Expired"})

                if(str(sotp.otp) == str(otp)):
                    try:
                        sotp.delete()
                    except:
                        return JsonResponse(status=500, data={'status': 'Failed', 'message':'Unable to verify OTP'})
                    else:
                        payload = {'phone':str(phone),}
                        jwt_token = jwt.encode(payload, config('SECRET_KEY'))
                        jwt_token = jwt_token.decode('utf-8')
                        return JsonResponse({"status": "Success", "message":"OTP Matched Successfully","token":jwt_token,"first login":gymuser.first_login})
                else:
                    return JsonResponse(status=404,data={'status': 'Failed', 'message':'OTP did not matched'})
            else:
                return JsonResponse(status=404,data={'status': 'Failed', 'message':'Please request OTP First'})
        else:
            return JsonResponse(status=404,data={'status': 'Failed', 'message':'User Not Found'})



@csrf_exempt
@gym_user
def get_profile(request, *args, **kwargs):
    if request.method=='GET':
        if(request.gymuser.first_login):
            return JsonResponse(status=200,data={"status":"Success","message":"Profile details not available"})
        return JsonResponse({"status":"Success",
                            'message':'Profile details fetched successfully',
                            'data':{'u_id':request.gymuser.u_id,
                                    'fname':request.gymuser.fname,
                                    'lname':request.gymuser.lname,
                                    'email':request.gymuser.email,
                                    'dob':request.gymuser.dob,
                                    'sex':request.gymuser.sex,
                                    'city':str(request.gymuser.city),
                                    'first_login':request.gymuser.first_login
                                    }
                            })



def get_date_from_str(dob):
     dob = dob.split('-')
     d = date(int(dob[0]), int(dob[1]), int(dob[2])) 
     return d

@csrf_exempt
@gym_user
def update_profile(request, *args, **kwargs):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        sex = request.POST.get('sex')
        city = request.POST.get('city')
        gymuser=request.gymuser
        gymuser.fname=fname
        gymuser.lname=lname
        gymuser.email=email
        gymuser.sex=sex
        try:
            cityObj = City.objects.get(city=city)
        except:
            return JsonResponse(status=404,data={'status': 'Profile Update Failed', 'message':'City Not Found'})
        else:
            gymuser.city=cityObj

        d = get_date_from_str(dob)
        gymuser.dob = d
        gymuser.first_login = False
        try:
            gymuser.save()
        except:
            return JsonResponse(status=500,data={'status': 'Profile Update Failed', 'message':'Some Error Occured'})
        else:
            return JsonResponse({'status':'Success', 'message':'Profile Updated Successfully'})
        

@csrf_exempt
@gym_user
def get_transaction_history(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            print(request.gymuser)
            transactions = Order.objects.filter(user=request.gymuser).order_by('-order_timestamp','-booking_id')
        except:
            return JsonResponse(status=500,data={'status':'Failed','message':'Some error occured'})
        else:
            if transactions.count() <= 0:
                return JsonResponse(status=404,data={'status':'Failed','message':'No Transaction Found'})
            else:
                transactionlist = []
                for tsc in transactions:
                    t = {}
                    t['booking_id']=tsc.booking_id
                    t['order_id']=tsc.order_id
                    t['payment_id']=tsc.payment_id
                    t['amount']=tsc.amount
                    t['count']=tsc.count
                    t['dom']=tsc.dom
                    t['gym']=str(tsc.gym.gymname)
                    t['booking date']=tsc.order_timestamp
                    t['expiry']=tsc.order_expiry
                    t['payment_status']=tsc.payment_status
                    t['payment_err_code']=tsc.payment_err_code
                    t['payment_err_msg']=tsc.payment_err_msg
                    transactionlist.append(t)
                return JsonResponse({'status':'Success','message':'All new Orders fetched', 'orders':transactionlist})
from django.http import JsonResponse
import jwt
from decouple import config
from user.models import GymUser
from gymowner.models import CredUser

def gym_user(function):
    def wrap(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION",None)
        if token is not None:
            try:
                payload = jwt.decode(token,config('SECRET_KEY'))
            except:
                return JsonResponse({'status':'Failed','message':'incorrect token'})
            else:
                phone = payload['phone']
                try:
                    gymuser = GymUser.objects.filter(phone = phone).first()
                except:
                    return JsonResponse({'status':'Failed','message':'User account not found'})
                else:
                    request.gymuser = gymuser
        else:
            return JsonResponse({'status':'Failed','message':'No Token Provided'})

        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def cred_user(function):
    def wrap(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION",None)
        if token is not None:
            try:
                payload = jwt.decode(token,config('SECRET_KEY'))
            except:
                return JsonResponse({'status':'Failed','message':'incorrect token'})
            else:
                username = payload['username']
                try:
                    creduser = CredUser.objects.filter(username = username).first()
                except:
                    return JsonResponse({'status':'Failed','message':'CredUser account not found'})
                else:
                    request.creduser = creduser
        else:
            return JsonResponse({'status':'Failed','message':'No Token Provided'})

        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

from django.contrib import admin

from .models import GymUser,City,State,OTP
# Register your models here.

admin.site.register(State)
admin.site.register(City)
admin.site.register(GymUser)
admin.site.register(OTP)

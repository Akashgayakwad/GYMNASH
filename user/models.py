from django.db import models
from django.core.validators import RegexValidator



class State(models.Model):
    state = models.CharField(max_length = 30)

    def __str__(self):
        return str(self.state)

class City(models.Model):
    city = models.CharField(max_length = 30)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.city)


def get_default_city():
    return City.objects.get(city="Raipur")

class GymUser(models.Model):
    phone_regex = RegexValidator(regex =r'^\+?1?\d{9,14}$',
        message="Phone number must be entered in format '+99999999' up to 14 digits")
    phone = models.CharField(validators = [phone_regex], max_length = 15, unique = True)
    u_id = models.AutoField(primary_key = True)
    fname = models.CharField(blank = True , null = True, max_length=20, verbose_name="First Name")
    lname = models.CharField(blank = True , null = True, max_length=20, verbose_name="Last Name")
    email = models.CharField(blank = True , null = True, max_length=40, verbose_name = "Email Address")
    dob = models.DateField(blank = True , null = True, verbose_name="Date Of Birth")
    sex = models.CharField(blank = True , null = True, max_length=6)
    city = models.ForeignKey(City,default=get_default_city,on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.phone)

    def get_username(self):
        return str(self.fname+" "+self.lname)

    def get_phone(self):
        return str(self.phone) 

    def get_city(self):
        return str(self.city)

class OTP(models.Model):
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    otp = models.IntegerField()
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.phone)+"-"+str(self.otp)



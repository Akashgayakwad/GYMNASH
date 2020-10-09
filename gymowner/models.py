from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models import City

class CredUser(AbstractUser):
    contact = models.BigIntegerField(null=True)
    aadhar = models.BigIntegerField(null=True)
    gymowner = models.BooleanField(default=False)


    def __str__(self):
        return str(self.first_name+self.last_name)

    class Meta:
        verbose_name = "CredUser"
        verbose_name_plural = "CredUsers"
    
    REQUIRED_FIELDS = ['email','first_name', 'last_name',]


def upload_logo_handler(instance, filename):
    return "gym_images/gym_{name}_{city}_{state}/logo/{file}".format(name=instance.gymname,city = str(instance.city), state= str(instance.city.state), file=filename)

def upload_images_handler(instance, filename):
    return "gym_images/gym_{name}_{city}_{state}/{file}".format(name=instance.gymname,city = str(instance.city), state= str(instance.city.state), file=filename)

class GYM(models.Model):
    gymname = models.CharField(max_length=50)
    gymowner = models.ForeignKey(CredUser,on_delete=models.CASCADE)
    logo = models.ImageField(upload_to= upload_logo_handler)
    image1 = models.ImageField(upload_to=upload_images_handler)
    image2 = models.ImageField(upload_to=upload_images_handler)
    image3 = models.ImageField(upload_to=upload_images_handler)
    image4 = models.ImageField(upload_to=upload_images_handler)
    image5 = models.ImageField(upload_to=upload_images_handler)
    feature1 = models.CharField(max_length=100)
    feature2 = models.CharField(max_length=100)
    feature3 = models.CharField(max_length=100)
    feature4 = models.CharField(max_length=100)
    feature5 = models.CharField(max_length=100)
    original_price = models.IntegerField()
    daily_price = models.IntegerField()
    monthly_price = models.IntegerField()
    two_monthly_price = models.IntegerField(default = -1)
    three_monthly_price= models.IntegerField(default = -1)
    four_monthly_price = models.IntegerField(default = -1)
    five_monthly_price = models.IntegerField(default = -1)
    six_monthly_price = models.IntegerField(default = -1)
    seven_monthly_price = models.IntegerField(default = -1)
    eight_monthly_price = models.IntegerField(default = -1)
    nine_monthly_price = models.IntegerField(default = -1)
    ten_monthly_price = models.IntegerField(default = -1)
    eleven_monthly_price = models.IntegerField(default = -1)
    twelve_monthly_price = models.IntegerField(default = -1)
    address = models.CharField(max_length=50)
    location = models.CharField(max_length=150)
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.gymname + ": " +str(self.city))

    def save(self, *args, **kwargs):
        if self.two_monthly_price == -1:
            self.two_monthly_price = self.monthly_price*2
        if self.three_monthly_price == -1:
            self.three_monthly_price = self.monthly_price*3
        if self.four_monthly_price == -1:
            self.four_monthly_price = self.monthly_price*4
        if self.five_monthly_price == -1:
            self.five_monthly_price = self.monthly_price*5
        if self.six_monthly_price == -1:
            self.six_monthly_price = self.monthly_price*6
        if self.seven_monthly_price == -1:
            self.seven_monthly_price = self.monthly_price*7
        if self.eight_monthly_price == -1:
            self.eight_monthly_price = self.monthly_price*8
        if self.nine_monthly_price == -1:
            self.nine_monthly_price = self.monthly_price*9
        if self.ten_monthly_price == -1:
            self.ten_monthly_price = self.monthly_price*10
        if self.eleven_monthly_price == -1:
            self.eleven_monthly_price = self.monthly_price*11
        if self.twelve_monthly_price == -1:
            self.twelve_monthly_price =self.monthly_price*12
        super().save(*args, **kwargs)
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
    address = models.CharField(max_length=50)
    location = models.CharField(max_length=150)
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.gymname + ": " +str(self.city))


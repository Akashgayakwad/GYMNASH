from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models import City

class CredUser(AbstractUser):
    contact = models.IntegerField(null=True)
    aadhar = models.IntegerField(null=True)
    gymowner = models.BooleanField(default=False)


    def __str__(self):
        return str(self.first_name+self.last_name)

    class Meta:
        verbose_name = "CredUser"
        verbose_name_plural = "CredUsers"
    
    REQUIRED_FIELDS = ['email','first_name', 'last_name',]


def upload_path_handler(instance, filename):
    return "gym_images/gym_{id}/{file}".format(id=instance.id, file=filename)

class GYM(models.Model):
    gymname = models.CharField(max_length=50)
    gymowner = models.ForeignKey(CredUser,on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to=upload_path_handler)
    image2 = models.ImageField(upload_to=upload_path_handler)
    image3 = models.ImageField(upload_to=upload_path_handler)
    image4 = models.ImageField(upload_to=upload_path_handler)
    image5 = models.ImageField(upload_to=upload_path_handler)
    price = models.IntegerField()
    address = models.CharField(max_length=50)
    location = models.CharField(max_length=150)
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.gymname + ": " +str(self.city))


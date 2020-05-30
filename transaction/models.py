from django.db import models
from django.core.validators import RegexValidator

from gymowner.models import GYM
from user.models import GymUser

class Order(models.Model):
    booking_id = models.BigAutoField(primary_key =True)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(null=True,max_length=100)
    payment_status = models.CharField(null=True,default="Pending",max_length=50)
    amount = models.IntegerField()
    months = models.IntegerField()
    gym = models.ForeignKey(GYM,on_delete=models.CASCADE)
    user = models.ForeignKey(GymUser,on_delete=models.CASCADE)
    new = models.BooleanField(default=True)

    def __str__(self):
        return str(str(self.user)+"-"+str(self.gym)+"-"+str(self.months)+":"+str(self.amount))
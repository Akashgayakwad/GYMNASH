from django.db import models
from django.core.validators import RegexValidator

from gymowner.models import GYM
from user.models import GymUser


class Order(models.Model):
    booking_id = models.BigAutoField(primary_key =True)
    order_id = models.CharField(max_length=100)
    amount = models.IntegerField()
    count = models.IntegerField()
    dom = models.BooleanField()
    gym = models.ForeignKey(GYM,on_delete=models.CASCADE)
    user = models.ForeignKey(GymUser,on_delete=models.CASCADE)
    new = models.BooleanField(default=True)
    order_timestamp = models.DateField(auto_now_add=True)
    order_expiry = models.DateField()
    payment_id = models.CharField(null=True,blank=True,max_length=100)
    payment_status = models.CharField(null=True,default="Pending",max_length=50)
    payment_err_code = models.CharField(null=True,blank=True,max_length=100)
    payment_err_msg = models.CharField(null=True,blank=True,max_length=200)

    def __str__(self):
        return str(str(self.user)+"-"+str(self.gym)+"-"+str(self.count)+":"+str(self.amount))

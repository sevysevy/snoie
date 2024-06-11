from django.db import models
from UserManagement.models import UserProfile , Organisation
from _shared.models import *

class AlertCanal(models.Model):

    name              = models.CharField(max_length=255)
    name_code         = models.CharField(max_length=255 , default="")
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)



# Create your models here.
class Alert(models.Model):
   
    num_order = models.CharField(max_length=255)


    alert_canal = models.ForeignKey(AlertCanal  , on_delete=models.SET_NULL, null=True)
    declaration    = models.TextField()
    date_alert     = models.DateTimeField()
    region         = models.ForeignKey(Region , on_delete=models.SET_NULL, null=True)
    department     = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    arrondissement = models.ForeignKey(Arrondissement , on_delete=models.SET_NULL, null=True)
    village        = models.CharField(max_length=255)
    informant_phone = models.CharField(max_length=100)

    user_profile     = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)
    organisation = models.ForeignKey(Organisation , on_delete=models.SET_NULL, null=True)

    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.num_order
    
    @staticmethod
    def get_num_order():
        last = Alert.objects.last()
        num = 0
        result =  "alert-{}".format(num)
        if last:
            num = last.id
            result = "alert-{}".format(num)

        return result



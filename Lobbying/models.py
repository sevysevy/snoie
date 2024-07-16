from django.db import models

from FicheManagement.models import FicheInformation, FichePertinence
from UserManagement.models import Organisation, UserProfile
from mission.models import Mission

# Create your models here.

class Lobby(models.Model):

    
    name                       = models.CharField(max_length=255 , default="") 
    user                       = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)

    organisation               = models.ForeignKey(Organisation , on_delete= models.SET_NULL, null=True)

    mission                    = models.ForeignKey(Mission , on_delete= models.SET_NULL, null=True)
    
    
    created_at                 =  models.DateTimeField(auto_now_add=True)
    updated_at                 =  models.DateTimeField(auto_now=True)


    
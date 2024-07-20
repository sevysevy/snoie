from django.db import models
from AlertsManagement.models import Alert
from FicheManagement.models import FicheInformation, FichePertinence
from UserManagement.models import UserProfile
from mission.models import Mission

# Create your models here.


class UserActionType(models.Model):

    name            = models.CharField(max_length=255)
    name_code       = models.CharField(max_length=255)
    category        = models.CharField(max_length=255)
    created_at      =  models.DateTimeField(auto_now_add=True)
    updated_at      =  models.DateTimeField(auto_now=True)


class UserAction(models.Model):
   
    action_type             = models.ForeignKey(UserActionType, on_delete=models.SET_NULL, null=True)
    autor                   = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)
    alert                   = models.ForeignKey(Alert , on_delete=models.SET_NULL, null=True)
    ficheInformation        = models.ForeignKey(FicheInformation , on_delete=models.SET_NULL, null=True)
    fichePertinence         = models.ForeignKey(FichePertinence , on_delete=models.SET_NULL, null=True)
    mission                 = models.ForeignKey(Mission , on_delete=models.SET_NULL, null=True)




    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)

    
    



class Comment(models.Model):
    title = models.CharField(max_length=255 , null=True)
    body  = models.TextField(null=True)
    action = models.ForeignKey(UserAction , on_delete=models.SET_NULL, null=True)
    autor                   = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_at   =  models.DateTimeField(auto_now=True)



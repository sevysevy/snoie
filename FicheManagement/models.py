from django.db import models

from UserManagement.models import Organisation, UserProfile
from _shared.models import *

# Create your models here.

class FicheInformation(models.Model):

    observator              = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)
    responsable             = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True , related_name="fi_res" )
    coordinator             = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True , related_name="fi_coord" )
    ref_fiche               = models.CharField(max_length=255 , default="")
    date_reception          = models.DateTimeField()
    date_constat            = models.DateTimeField()
    organisation            = models.ForeignKey(Organisation , on_delete=models.SET_NULL, null=True)
    entite                  = models.CharField(max_length=255 , default="")
    village                 = models.CharField(max_length=255 , default="")
    region                  = models.ForeignKey(Region , on_delete=models.SET_NULL, null=True)
    department              = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    arrondissement          = models.ForeignKey(Arrondissement , on_delete=models.SET_NULL, null=True)
    title_exploitation      = models.CharField(max_length=255 , default="")
    exploitant_name         = models.CharField(max_length=255 , default="")
    infraction_description  = models.TextField(default="")
    soupicious_infraction   = models.TextField(default="")
    ref_legislation_text    = models.TextField(default="")
    sign_obs                = models.TextField(default="")
    date_sign_obs            = models.DateTimeField(null=True)

    sign_resp                = models.TextField(default="")
    date_sign_resp           = models.DateTimeField(null=True)

    sign_coord               = models.TextField(default="")
    date_sign_coord            = models.DateTimeField(null=True)

    state                   = models.CharField(max_length=255 , default="")
    created_at              =  models.DateTimeField(auto_now_add=True)
    updated_at              =  models.DateTimeField(auto_now=True)



class FichePertinence(models.Model):

    
    observator                  = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="observator")
    ref_fiche                   = models.CharField(max_length=255 , default="")
    date_renseignement          = models.DateTimeField()
    date_demarage               = models.DateTimeField(null=True)
    contexte                    = models.TextField(default="")
    domain                      = models.CharField(max_length=255 , default="")
    denonciateur                = models.CharField(max_length=255 , default="")
    organisation                = models.ForeignKey(Organisation , on_delete=models.SET_NULL, null=True)
    designation                 = models.TextField(default="")
    pertinence                  = models.BooleanField(default=False)
    access_site                 = models.BooleanField(default=False)
    activity_state              = models.CharField(max_length=255 , default="")
    state                       = models.CharField(max_length=255 , default="")
    justif                      = models.BooleanField(default=False)
    nature                      = models.CharField(max_length=255 , default="")
    severity_level              = models.CharField(max_length=255 , default="")
    severity_justif             = models.CharField(max_length=255 , default="")
    profit_level                = models.CharField(max_length=255 , default="")
    sign_resp                   = models.TextField(default="")
    sign_coor                   = models.TextField(default="")
    sign_obs                    = models.TextField(default="")
    date_sign_resp              = models.DateTimeField(null=True)
    date_sign_coo               = models.DateTimeField(null=True)
    date_sign_obs               = models.DateTimeField(null=True)
    coordinator                 = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="coordinator")
    responsable                 = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="responsable")
    observation_coor            = models.TextField(default="")
    observation_resp            = models.TextField(default="")
    fiche_information           = models.ForeignKey(FicheInformation , on_delete=models.SET_NULL, null=True)
    priority                    = models.CharField(max_length=255 , default="")
    status                      = models.CharField(max_length=255 , default="")
    encours_activite            = models.BooleanField(default=False)
    arret_activite              = models.BooleanField(default=False)
    niveau                      = models.BooleanField(default=False)
    niveauSeverite              = models.IntegerField(default=False)

    created_at                  =  models.DateTimeField(auto_now_add=True)
    updated_at                  =  models.DateTimeField(auto_now=True)
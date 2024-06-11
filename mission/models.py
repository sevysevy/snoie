from django.db import models

from FicheManagement.models import FicheInformation, FichePertinence
from UserManagement.models import Organisation, UserProfile

# Create your models here.

class Mission(models.Model):

    
    name                            = models.CharField(max_length=255 , default="") 
    user                            = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)
    pv_entretient                   = models.FileField(upload_to="mission_doc")
    compte_rendu_entretient         = models.FileField(upload_to="mission_doc")
    check_list_conformite           = models.FileField(upload_to="mission_doc")
    rapport_mission                 = models.FileField(upload_to="mission_doc")
    fiche_observation               = models.FileField(upload_to="mission_doc")
    organisation                    = models.ForeignKey(Organisation , on_delete= models.SET_NULL, null=True)
    fiche_information               = models.ForeignKey(FicheInformation , on_delete=models.SET_NULL, null=True)
    fiche_pertinence                = models.ForeignKey(FichePertinence, on_delete=models.SET_NULL, null=True)
    draft_tdr                       = models.FileField(upload_to="mission_doc")
    tdr_valid                       = models.FileField(upload_to="mission_doc")
    ordre_mission                   = models.FileField(upload_to="mission_doc")
    tdr_amender                     = models.FileField(upload_to="mission_doc")
    statut_mission                  = models.CharField(max_length=255, default="")
    rapport_mission_approuve        = models.FileField(upload_to="mission_doc")
    rapport_mission_amende_2        = models.FileField(upload_to="mission_doc")
    rapport_mission_amende_1        = models.FileField(upload_to="mission_doc")
    plan_lobbying                   = models.FileField(upload_to="mission_doc")
    rapport_mission_commente        = models.TextField(default="")
    comment_cancel                  = models.TextField(default="")
    motif_annulation                = models.TextField(default="")
    statut_commentaire              = models.TextField(default="")

    
    created_at                  =  models.DateTimeField(auto_now_add=True)
    updated_at                  =  models.DateTimeField(auto_now=True)
from django.db import models

from FicheManagement.models import FicheInformation, FichePertinence
from UserManagement.models import Organisation, UserProfile

# Create your models here.

class Mission(models.Model):

    
    name                            = models.CharField(max_length=255 , default="") 
    user                            = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)

    organisation                    = models.ForeignKey(Organisation , on_delete= models.SET_NULL, null=True)
    fiche_information               = models.ForeignKey(FicheInformation , on_delete=models.SET_NULL, null=True)
    fiche_pertinence                = models.ForeignKey(FichePertinence, on_delete=models.SET_NULL, null=True)


    pv_entretient                   = models.FileField(upload_to="mission_doc")
    date_pv_entretien               = models.DateTimeField(null=True)
    user_pv_entretien               = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="pv_entretien")

    compte_rendu_entretient         = models.FileField(upload_to="mission_doc")
    date_compte_rendu_entretien               = models.DateTimeField(null=True)
    user_compte_rendu_entretien               = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="compte_rendu_entretien")

    check_list_conformite           = models.FileField(upload_to="mission_doc")
    date_check_list               = models.DateTimeField(null=True)
    user_check_list               = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="check_list")
    
    fiche_observation             = models.FileField(upload_to="mission_doc")
    date_fiche_observation               = models.DateTimeField(null=True)
    user_fiche_observation               = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="fiche_observation")
    
    draft_tdr                       = models.FileField(upload_to="mission_doc")
    date_draft_tdr                  = models.DateTimeField(null=True)
    user_draft_tdr                  = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="draft_tdr")

    tdr_valid                       = models.FileField(upload_to="mission_doc")
    date_tdr_valid                  = models.DateTimeField(null=True)
    user_tdr_valid                  = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="tdr_valid")

    ordre_mission                   = models.FileField(upload_to="mission_doc")
    date_ordre_mission                  = models.DateTimeField(null=True)
    user_ordre_mission                 = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="ordre_mission")

    tdr_amender                     = models.FileField(upload_to="mission_doc")
    date_tdr_amender                  = models.DateTimeField(null=True)
    user_tdr_amender                = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="tdr_amender")

    

    rapport_mission                 = models.FileField(upload_to="mission_doc")
    date_rapport_mission                  = models.DateTimeField(null=True)
    user_rapport_mission                = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="rapport_mission")

    rapport_mission_commente        = models.FileField(upload_to="mission_doc")
    date_mission_commente           = models.DateTimeField(null=True)
    user_mission_commente           = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="rapport_mission_commente")

    rapport_mission_approuve        = models.FileField(upload_to="mission_doc")
    date_mission_approuve           = models.DateTimeField(null=True)
    user_mission_approuve           = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="rapport_mission_approuve")

    rapport_mission_amende_2        = models.FileField(upload_to="mission_doc")
    date_mission_amende_2          = models.DateTimeField(null=True)
    user_mission_amende_2          = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="rapport_mission_amende_2")

    rapport_mission_amende_1        = models.FileField(upload_to="mission_doc")
    date_mission_amende_1          = models.DateTimeField(null=True)
    user_mission_amende_1          = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="rapport_mission_amende_1")

    plan_lobbying                   = models.FileField(upload_to="mission_doc")
    date_plan_lobbying              = models.DateTimeField(null=True)
    user_plan_lobbying              = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True , related_name="plan_lobbying")
    
    comment_cancel                  = models.TextField(default="")
    motif_annulation                = models.TextField(default="")
    statut_commentaire              = models.TextField(default="")
    statut_mission                  = models.CharField(max_length=255, default="")
    
    date_mission_start              = models.DateTimeField(null=True)
    date_mission_end                = models.DateTimeField(null=True)
    date_mission_cancel             = models.DateTimeField(null=True)
    
    created_at                  =  models.DateTimeField(auto_now_add=True)
    updated_at                  =  models.DateTimeField(auto_now=True)
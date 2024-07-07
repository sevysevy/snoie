from django.shortcuts import redirect, render 
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse
from UserManagement.models import UserProfile
from FicheManagement.models import *
from _shared.models import *
from django.http import JsonResponse , HttpResponseBadRequest , HttpResponseServerError, FileResponse, Http404 
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date , datetime
from io import BytesIO
from PIL import Image
import base64

from mission.models import Mission

# Create your views here.
@login_required
def mission_registry(request , page):

    user_profile = request.user.userprofile

    missions = Mission.objects.filter().order_by('id').reverse()

    paginator = Paginator(missions , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    context = {"missions": page_objects}
    
    return render(request , "mission/registry.html" , context)


@login_required
def start_mission(request , id):

    user_profile = request.user.userprofile

    if request.method == 'POST':

        mission = Mission.objects.filter(id = id)
        mission.statut_mission = "running"

        mission.save()
        
    context = {"message": "mision started succefully"}
    
    return JsonResponse(context)


@login_required
def create_mission(request):
    user = request.user.userprofile

    if request.method == "POST":
        try:
            
            mission_name = request.POST.get("nom_mission")
            fp_id = request.POST.get("fp")
            draft_tdr = request.FILES.get("draft_tdr")

            fp = FichePertinence.objects.get(id=fp_id)
            mission = Mission(name = mission_name , fiche_pertinence = fp , fiche_information = fp.fiche_information , draft_tdr = draft_tdr , user = user , statut_mission = "pending" , organisation = user.organisation , user_draft_tdr=user , date_draft_tdr = date.today())
            mission.save()

            return redirect("mission-registry" , 1 )
        except Exception as e:
           return HttpResponseServerError("Une erreur est survenue lors de l'enregistrement.")

        
    mission_count = Mission.objects.all().count() + 1

    fiche_pertinence = [{"id": elm.id , "ref":elm.ref_fiche} for elm in FichePertinence.objects.filter(organisation = user.organisation ,  state = "validated_coord" , mission = None)]
    mission_name = ""

    

    if len(str(mission_count)) <= 2:
        mission_name = "00"+str(mission_count) + "/RO-SNOIE/" + str.upper(user.organisation.name) + "/" + date.strftime(date.today() , "%m%Y")
        
    else:
        mission_name = "0"+str(mission_count) + "/RO-SNOIE/" + str.upper(user.organisation.name) + "/"  + date.strftime(date.today() , "%m%Y")    

    context = {"mission_name" : mission_name , "fp":fiche_pertinence}

    return JsonResponse(context)




def detail_mission(request, id):


   
    mission = Mission.objects.get(id=id)
    step = 1


    context = {"mission":mission ,   "step":step  }

    return render(request , "mission/mission_details.html" , context)




def download_mission_doc(request, id):
    doc_type = request.GET.get('doc-type' , None)

    if doc_type:
        mission = Mission.objects.get(id=id)

        file_path = ""

        if doc_type == 'draft-tdr':

            file_path = mission.draft_tdr.path

        elif doc_type == 'tdr-amender':
            file_path = mission.tdr_amender.path

        elif doc_type == 'tdr-valid':
            file_path = mission.tdr_valid.path
            

        elif doc_type == 'ordre-mission':
            file_path = mission.ordre_mission.path
            
        elif doc_type == 'pv-entretien':
            file_path = mission.pv_entretient.path

        elif doc_type == 'compte-rd-entretien':
            file_path = mission.compte_rendu_entretient.path

        elif doc_type == 'fiche-observation':
            file_path = mission.fiche_observation.path

        elif doc_type == 'check-list-conform':

            file_path = mission.check_list_conformite.path

        elif doc_type == 'rapport-mission':
            file_path = mission.rapport_mission.path

        elif doc_type == 'rapport-mission-commente':
            file_path = mission.rapport_mission_commente.path


        elif doc_type == 'rapport-mission-amender-1':
            file_path = mission.rapport_mission_amende_1.path

        elif doc_type == 'rapport-mission-amender-2':
            file_path = mission.rapport_mission_amende_2.path

        elif doc_type == 'rapport-mission-approuver':
            file_path = mission.rapport_mission_approuve.path

        
        response = FileResponse(open(file_path , 'rb'))

        response['Content-Disposition'] = f'attachment; filename="{mission.name + "_" +str.upper(doc_type)}"'

        return response
    

    raise Http404



def add_mission_doc(request, id):
    user = request.user.userprofile

    if request.method == "POST":
        print(request.POST)
        doc_type = request.POST.get('doc-type' , None)

        if doc_type:
            mission = Mission.objects.get(id=id)

            if doc_type == 'tdr-amender':
                mission.tdr_amender = request.FILES.get("document")
                mission.user_tdr_amender = user
                mission.date_tdr_amender = date.today()

            elif doc_type == 'tdr-valid':
                mission.tdr_valid = request.FILES.get("document")
                mission.user_tdr_valid = user
                mission.date_tdr_valid = date.today()

            elif doc_type == 'ordre-mission':
                mission.ordre_mission = request.FILES.get("document")
                mission.user_ordre_mission = user
                mission.date_ordre_mission = date.today()

            elif doc_type == 'pv-entretien':
                mission.pv_entretient = request.FILES.get("document")
                mission.user_pv_entretien = user
                mission.date_pv_entretien = date.today()

            elif doc_type == 'compte-rd-entretien':
                mission.compte_rendu_entretient = request.FILES.get("document")
                mission.user_compte_rendu_entretien = user
                mission.date_compte_rendu_entretien = date.today()

            elif doc_type == 'fiche-observation':
                mission.fiche_observation = request.FILES.get("document")
                mission.user_fiche_observation = user
                mission.date_fiche_observation = date.today()

            elif doc_type == 'check-list-conform':

                mission.check_list_conformite = request.FILES.get("document")
                mission.user_check_list = user
                mission.date_check_list = date.today()

            elif doc_type == 'rapport-mission':
                mission.rapport_mission = request.FILES.get("document")
                mission.user_rapport_mission = user
                mission.date_rapport_mission = date.today()

            elif doc_type == 'rapport-mission-commente':
                mission.rapport_mission_commente = request.FILES.get("document")
                mission.user_mission_commente = user
                mission.date_mission_commente = date.today()


            elif doc_type == 'rapport-mission-amender-1':
                mission.rapport_mission_amende_1 = request.FILES.get("document")
                mission.user_mission_amende_1 = user
                mission.date_mission_amende_1 = date.today()

            elif doc_type == 'rapport-mission-amender-2':
                mission.rapport_mission_amende_2 = request.FILES.get("document")
                mission.user_mission_amende_2 = user
                mission.date_mission_amende_2 = date.today()

            elif doc_type == 'rapport-mission-approuver':
                mission.rapport_mission_approuve = request.FILES.get("document")
                mission.user_mission_approuve = user
                mission.date_mission_approuve = date.today()


            mission.save()

            
            redirect_url = reverse('detail-mission',  kwargs={'id': 1},)
            return redirect(redirect_url)  
    

    raise HttpResponseBadRequest
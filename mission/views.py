from django.shortcuts import redirect, render 
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from UserManagement.models import UserProfile
from FicheManagement.models import *
from _shared.models import *
from django.http import JsonResponse , HttpResponseBadRequest , HttpResponseServerError
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

    missions = Mission.objects.filter()

    paginator = Paginator(missions , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    context = {"missions": page_objects}
    
    return render(request , "mission/registry.html" , context)



@login_required
def create_mission(request):
    user = request.user.userprofile

    if request.method == "POST":
        try:
            
            mission_name = request.POST.get("nom_mission")
            fp_id = request.POST.get("fp")
            draft_tdr = request.FILES.get("draft_tdr")

            fp = FichePertinence.objects.get(id=fp_id)
            mission = Mission(name = mission_name , fiche_pertinence = fp , draft_tdr = draft_tdr , user = user , statut_mission = "pending" , organisation = user.organisation )
            mission.save()

            return redirect("mission-registry" , 1 )
        except Exception as e:
           return HttpResponseServerError("Une erreur est survenue lors de l'enregistrement.")

        



    mission_count = Mission.objects.all().count() + 1

    fiche_pertinence = [{"id": elm.id , "ref":elm.ref_fiche} for elm in FichePertinence.objects.filter(organisation = user.organisation)]
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
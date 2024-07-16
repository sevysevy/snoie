from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from Lobbying.models import Lobby
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
def lobby_registry(request , page):

    user_profile = request.user.userprofile

    if user_profile.role.name_code ==  "coordonnator":
        lobbys = Mission.objects.filter(statut_mission = "ended").order_by('id').reverse()
    else:
        lobbys = Lobby.objects.filter(organisation = user_profile.organisation).order_by('id').reverse()

    

    paginator = Paginator(lobbys , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    context = {"lobbys": page_objects}
    
    return render(request , "lobbying/registry.html" , context)


@login_required
def lobby_details(request, id):


   
    mission = Mission.objects.get(id=id)
    step = 1


    context = {"mission":mission ,   "step":step  }

    return render(request , "lobbying/lobby_details.html" , context)
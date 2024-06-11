from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def get_departments(request):

    user_profile = request.user.userprofile
    region_id = request.GET.get("region_id" , None)
    region = None
    departments =[]

    if region_id != None:
        region = Region.objects.get(id=region_id)

        departments = list(Department.objects.filter(region = region).values("id" , "name"))



    context = {"departments" : departments}

    return JsonResponse(context)


@login_required
def get_arr(request):

    department_id = request.GET.get("department_id" , None)
    department = None
    arrs =[]

    if department_id != None:
        department = Department.objects.get(id=department_id)

        arrs = list(Arrondissement.objects.filter(department = department).values())

    context = {"arrs" : arrs}

    return JsonResponse(context)
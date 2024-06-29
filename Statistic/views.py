from datetime import date
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from AlertsManagement.models import *
from FicheManagement.models import FicheInformation, FichePertinence
# Create your views here.


@login_required
def statistic_alert(request):

    return render(request , "statistic/alert.html")



@login_required
def statistic_alert_datas(request):

    start = request.GET.get('start',"1970-01-01")
    end = request.GET.get('end', date.today().strftime("%Y-%m-%d"))

    print(start)
    print(end)

    
    number_alert = Alert.objects.filter(created_at__date__range = (start , end)).count() 
    alerts = Alert.objects.filter(created_at__date__range = (start , end))
    print(alerts)
    canals = AlertCanal.objects.all()
    regions = Region.objects.all().order_by('name')
    alert_by_month = {}
    alert_by_canals = {}
    alert_by_region = {}

    for i in range(1,13):
        alert_by_month[str(i)] = 0

        for elm in alerts:
            if elm.created_at.month == i:
                alert_by_month[str(i)] = alert_by_month[str(i)] + 1

    
    for elm in canals:
        alert_by_canals[elm.name] = 0

        for val in alerts:
            if val.alert_canal.name_code == elm.name_code:
                alert_by_canals[elm.name] = alert_by_canals[elm.name] + 1

    for elm in regions:
        alert_by_region[elm.name] = 0

        for val in alerts:
            if val.region.name_code == elm.name_code:
                alert_by_region[elm.name] = alert_by_region[elm.name] + 1


    context = {"num_alerts": number_alert,
               "alerts_by_months": alert_by_month,
               "alerts_by_canals" : alert_by_canals,
               "alerts_by_regions": alert_by_region
               }
    
    return JsonResponse(context)

    


@login_required
def statistic_fiche(request):

    
    return render(request , "statistic/fiche.html" )




@login_required
def statistic_fiche_datas(request):

    start = request.GET.get('start',"1970-01-01")
    end = request.GET.get('end', date.today().strftime("%Y-%m-%d"))

    fiche_info = FicheInformation.objects.filter(created_at__date__range = (start , end))
    fiche_perti = FichePertinence.objects.filter(created_at__date__range = (start , end))

    number_fi = fiche_info.count()
    number_fp = fiche_perti.count()

    
    org = Organisation.objects.all()
    regions = Region.objects.all().order_by('name')

    fi_by_month = {}
    fp_by_month = {}

    fi_by_org = {}
    fp_by_org = {}

    fi_by_region = {}
    fp_by_region = {}
    

    for i in range(1,13):
        fi_by_month[str(i)] = 0
        fp_by_month[str(i)] = 0

        for elm in fiche_info:
            if elm.created_at.month == i:
                fi_by_month[str(i)] = fi_by_month[str(i)] + 1

        for el in fiche_perti:
            if el.created_at.month == 1:
                fp_by_month[str(i)] = fp_by_month[str(i)] + 1

    

    for elm in regions:
        fi_by_region[elm.name] = 0
        fp_by_region[elm.name] = 0

        for val in fiche_info:
            if val.region.name_code == elm.name_code:
                fi_by_region[elm.name] = fi_by_region[elm.name] + 1

        for va in fiche_perti:
            if va.fiche_information.region.name_code == elm.name_code:
                fp_by_region[elm.name] = fp_by_region[elm.name] + 1


    for elm in org:
        fi_by_org[elm.name] = 0
        fp_by_org[elm.name] = 0

        for val in fiche_info:
            if val.organisation.name == elm.name:
                fi_by_org[elm.name] = fi_by_org[elm.name] + 1

        for va in fiche_perti:
            if va.organisation.name == elm.name:
                fp_by_org[elm.name] = fp_by_org[elm.name] + 1


    context = {"number_fi": number_fi, "number_fp":number_fp, "fi_by_months":fi_by_month, "fp_by_months":fp_by_month,
               "fi_by_regions":fi_by_region , "fp_by_regions":fp_by_region , "fi_by_orgs":fi_by_org}
    
    return JsonResponse(context)



@login_required
def statistic_mission(request):

    user_profile = request.user.userprofile

    context = {}
    
    return render(request , "statistic/mission.html" , context)


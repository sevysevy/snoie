from datetime import date
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from AlertsManagement.models import *
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

    user_profile = request.user.userprofile

    context = {}
    
    return render(request , "statistic/fiche.html" , context)


@login_required
def statistic_mission(request):

    user_profile = request.user.userprofile

    context = {}
    
    return render(request , "statistic/mission.html" , context)


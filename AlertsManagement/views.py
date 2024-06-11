from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from UserManagement.models import UserProfile
from AlertsManagement.models import *
from _shared.models import *
from django.http import JsonResponse , HttpResponseBadRequest , HttpResponseServerError
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required
def alert_registry(request , page):

    user_profile = request.user.userprofile


    alerts = Alert.objects.filter(organisation = user_profile.organisation)

    paginator = Paginator(alerts , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    context = {"alerts": page_objects}
    


    return render(request , "alerts/registry.html" , context)


@login_required
def create_alert(request):

    user_profile = request.user.userprofile
    regions = Region.objects.all().order_by('name')
    canals = AlertCanal.objects.all().order_by('name')
    step = request.GET.get("step", None)

    context = {'regions':regions , 'canals':canals }

    if request.method == "POST":
        step = request.POST.get("step" , None)
       
        if step == "1":
            try:
                declaration = request.POST.get('alert_declaration')
                date_alert = request.POST.get('date_alert')
                num_order  = Alert.get_num_order()

                alert = Alert.objects.create(num_order=num_order , declaration=declaration , date_alert = date_alert , user_profile = user_profile , organisation = user_profile.organisation)
                request.session['alert_id'] = alert.id
                step = "2"

                context = {'alert_id':alert.id , "next-step":"2"}
                return JsonResponse(context)
            except Exception as e:
                print(e)
                context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")


        if step == "2":
            try:
                region_id = request.POST.get('region')
                department_id = request.POST.get('department')
                arrondissement_id = request.POST.get('arrondissement')
                village = request.POST.get('village')

                if 'alert_id' in request.session:
                    id = request.session['alert_id']
                    try:
                        alert = Alert.objects.get(id = id , user_profile = request.user.userprofile)
                        region = Region.objects.get(id = region_id)
                        department = Department.objects.get(id = department_id)
                        arr = Arrondissement.objects.get(id = arrondissement_id)
                        
                        alert.region = region
                        alert.department = department
                        alert.arrondissement = arr
                        alert.village = village
                       
                        alert.save()
                        step = "3"

                        context = {'alert_id':alert.id , "next-step": "3"}
                        
                    except Exception as e:
                        print(e)
                        context.update({'error':'Impossible de trouver cette alerte'})
                        return HttpResponseBadRequest("Impossible de trouver cette alerte")

                    return JsonResponse(context)

                context = {'alert_id':alert.id , "next-step":"2"}
                return JsonResponse(context)
            except Exception as e:
                print(e)
                context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")

        if step == "3":
            print(request.POST)
            try:
                canal = request.POST.get('canal')
                tel_informateur = request.POST.get('tel-informateur')

                if 'alert_id' in request.session:
                    id = request.session['alert_id']

                    try:
                        alert = Alert.objects.get(id = id , user_profile = request.user.userprofile)
                        alert_canal = AlertCanal.objects.get(id = canal)

                        alert.alert_canal = alert_canal
                        alert.informant_phone = tel_informateur
                        
                        alert.save()
                        step = "3"

                        context = {'alert_id':alert.id }
                        
                    except Exception as e:
                        print(e)
                        context.update({'error':'Impossible de trouver cette alerte'})
                        return HttpResponseBadRequest("Impossible de trouver cette alerte")

                    return JsonResponse(context)

            except Exception as e:
                print(e)
                context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")


       
    if not step:
        if 'alert_id' in request.session:
            del request.session['alert_id']
        return render(request , "alerts/create_alert.html" , context)
    






@login_required
def view_update_alert(request, id):
    try:

        if request.method == "POST":
            print(request.POST)
            step = request.POST.get("step")

            if step == "1":
                
                try:
                    declaration = request.POST.get('alert_declaration')
                    date_alert = request.POST.get('date_alert')
                    id = request.POST.get("alert_id")

                    alert = Alert.objects.get(id = id)
                    alert.declaration = declaration
                    alert.date_alert = date_alert

                    alert.save()

                    step = "2"

                    context = {"next-step":"2"}
                    return JsonResponse(context)
                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")

            if step == "2":
                try:
                    region_id = request.POST.get('region')
                    department_id = request.POST.get('department')
                    arrondissement_id = request.POST.get('arrondissement')
                    village = request.POST.get('village')
                    id = request.POST.get("alert_id")

                   
                    alert = Alert.objects.get(id = id)
                    region = Region.objects.get(id = region_id)
                    department = Department.objects.get(id = department_id)
                    arr = Arrondissement.objects.get(id = arrondissement_id)
                    
                    alert.region = region
                    alert.department = department
                    alert.arrondissement = arr
                    alert.village = village
                
                    alert.save()
                    step = "3"

                    context = {"next-step": "3"}
                            

                    return JsonResponse(context)

                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")


            if step == "3":
                try:
                    canal = request.POST.get('canal')
                    tel_informateur = request.POST.get('tel-informateur')
                    id = request.POST.get("alert_id")

                    alert = Alert.objects.get(id = id)
                    alert_canal = AlertCanal.objects.get(id = canal)
                    alert.alert_canal = alert_canal
                    alert.informant_phone = tel_informateur
                    
                    alert.save()
                    context = {'alert_id':alert.id }
                    return JsonResponse(context)
                            
                  
                        

                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")


        regions = Region.objects.all().order_by('name')
        canals = AlertCanal.objects.all().order_by('name')
        mode = request.GET.get('mode' , None)

        if mode is None:
            mode = 'view'

        alert = Alert.objects.get(id=id)
        dep_id = alert.department.id
        arr_id = alert.arrondissement.id
        step = 1

        context = {'regions':regions , 'canals':canals , 'alert':alert , 'mode':mode , 'dep_id': dep_id , 'arr_id':arr_id , "step":step}

        return render(request , "alerts/view_update_alert.html" , context)

    except Exception as e:
        print(e)
        return HttpResponseServerError(e)







@login_required
def get_alert_info(request , id):

    user_profile = request.user.userprofile

    alert = Alert.objects.filter(user_profile = user_profile , id=id).first()
    html = ""
    if alert:
        html = render_to_string( "alerts/alert-info.html" , {"alert" : alert})
        
    return JsonResponse({"html": html})



def delete_alert(request):
    if request.method == 'POST':
        id = request.POST.get("alert_id")
        alert = Alert.objects.get(id = id)

        alert.delete()

        return JsonResponse({"status": "deleted"})
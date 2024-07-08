from django.shortcuts import render 
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

# Create your views here.
@login_required
def fiche_info_registry(request , page):

    user_profile = request.user.userprofile

    if user_profile.role.name_code ==  "coordonnator":
        fiches = FicheInformation.objects.filter( state__in = ["validated_org" , "validated_coord"] ).order_by('id').reverse()
    else:
        fiches = FicheInformation.objects.filter(organisation = user_profile.organisation).order_by('id').reverse()

    

    paginator = Paginator(fiches , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    context = {"fiches": page_objects}
    
    return render(request , "fiche-info/registry.html" , context)


@login_required
def get_fiches_info(request):

    user_profile = request.user.userprofile


    fiches = FicheInformation.objects.filter( organisation = user_profile.organisation , state = "validated_org" , fichepertinence__fiche_information = None)
    print(fiches)
    if fiches.count() > 0:
        context = {"fiches": [{"id" : elm.id , "ref" : elm.ref_fiche} for elm in fiches ]}
    else:
        context = {"fiches":[]}

    return JsonResponse(context)

    


@login_required
def create_fiche_info(request ):


    user_profile = request.user.userprofile

    if request.method == "POST":
        print(request.POST)
        step = request.POST.get("step")
        context = {}
        if step == "1":
            try:
                ref_fi = request.POST.get("ref_fi")
                date_constat = request.POST.get("date_constat")
                date_reception = request.POST.get("date_reception")
                entite = request.POST.get("entite")

                fiche = FicheInformation.objects.create(ref_fiche = ref_fi , date_constat = date_constat , date_reception = date_reception , entite = entite, organisation = user_profile.organisation , observator = user_profile , state="draft")
                
                request.session['fi_id'] = fiche.id
                step = "2"
                context = {'fi_id':fiche.id , "next-step":step}

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
                village = request.POST.get('village_fi')
                titre_exp  = request.POST.get('titre_exp')
                
               
                if 'fi_id' in request.session:
                    id = request.session['fi_id']
                    try:
                        fiche = FicheInformation.objects.get(id = id)
                        region = Region.objects.get(id = region_id)
                        department = Department.objects.get(id = department_id)
                        arr = Arrondissement.objects.get(id = arrondissement_id)
                        
                        fiche.region = region
                        fiche.department = department
                        fiche.arrondissement = arr
                        fiche.village = village
                        fiche.title_exploitation = titre_exp
                       
                        fiche.save()
                        step = "3"

                        context = {'fi_id':fiche.id , "next-step": step}
                        
                    except Exception as e:
                        print(e)
                        context.update({'error':'Impossible de trouver cette fiche'})
                        return HttpResponseBadRequest("Impossible de trouver cette fiche")

                    return JsonResponse(context)

                raise HttpResponseBadRequest ("fiche introuvable !!!")
            except Exception as e:
                print(e)
                context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")

        if step == "3":
            try:
                nom_exp = request.POST.get('nom_exp')
                desc_ex_fi = request.POST.get('desc_ex_fi')
                soup_fi = request.POST.get('soup_fi')
                ref_text_leg = request.POST.get('ref_text_leg')
                
               
                if 'fi_id' in request.session:
                    id = request.session['fi_id']
                    try:
                        fiche = FicheInformation.objects.get(id = id)
                        
                        fiche.exploitant_name = nom_exp
                        fiche.infraction_description = desc_ex_fi
                        fiche.soupicious_infraction = soup_fi
                        fiche.ref_legislation_text = ref_text_leg
                       
                        fiche.save()
                        step = "4"

                        context = {'fi_id':fiche.id , "next-step": step}
                        
                    except Exception as e:
                        print(e)
                        context.update({'error':'Impossible de trouver cette fiche'})
                        return HttpResponseBadRequest("Impossible de trouver cette fiche")

                    return JsonResponse(context)

                raise HttpResponseBadRequest ("fiche introuvable !!!")
            except Exception as e:
                print(e)
                context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")

        if step == "4":
            if 'fi_id' in request.session:
                id = request.session['fi_id']
                try:
                    signature = request.POST.get('signed')

                    fiche = FicheInformation.objects.get(id = id)
                    
                    fiche.sign_obs = signature
                    fiche.date_sign_obs = date.today()
                    fiche.state = "send_to_resp" 

                    fiche.save()
                    context = {'fi_id':fiche.id , "next-step": "5"}
                    return JsonResponse(context)
                except Exception as e:
                    print(e)
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")

    
    ref_fi = 0
    last_id = 1 
    step = 1
    regions = Region.objects.all().order_by('name')
    if FicheInformation.objects.last() :
        last_id = FicheInformation.objects.last().id + 1

    if len(str(last_id)) < 2:
        ref_fi = "00"+str(last_id) + "-FI-SNOIE-" + str.upper(user_profile.organisation.name) + "-" + date.strftime(date.today() , "%m%Y")
    else:
        ref_fi = "0"+str(last_id) + "-FI-SNOIE-" + str.upper(user_profile.organisation.name) + "-" + date.strftime(date.today() , "%m%Y")    

    organisation = user_profile.organisation



    context = {"ref_fi" : ref_fi , "organisation": organisation , "step": step , "regions":regions}

    return render(request , "fiche-info/create_fiche_info.html" , context)




@login_required
def view_update_fi(request, id):
    try:

        if request.method == "POST":
            #print(request.POST)
            step = request.POST.get("step")
            context = {}
            
            
            
            if step == "1":
                try:
                    date_constat = request.POST.get("date_constat")
                    date_reception = request.POST.get("date_reception")
                    entite = request.POST.get("entite")
                    

                    fiche = FicheInformation.objects.get(id = id)
                    fiche.date_constat = date_constat
                    fiche.date_reception = date_reception
                    fiche.entite = entite

                    fiche.save()
                    step = "2"
                    context = {"next-step":step}

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
                    village = request.POST.get('village_fi')
                    titre_exp  = request.POST.get('titre_exp')
                    
                
                    try:
                        fiche = FicheInformation.objects.get(id = id)
                        region = Region.objects.get(id = region_id)
                        department = Department.objects.get(id = department_id)
                        arr = Arrondissement.objects.get(id = arrondissement_id)
                        
                        fiche.region = region
                        fiche.department = department
                        fiche.arrondissement = arr
                        fiche.village = village
                        fiche.title_exploitation = titre_exp
                    
                        fiche.save()
                        step = "3"

                        context = {'fi_id':fiche.id , "next-step": step}
                        
                    except Exception as e:
                        print(e)
                        context.update({'error':'Impossible de trouver cette fiche'})
                        return HttpResponseBadRequest(e)

                    return JsonResponse(context)

                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")
            
            if step == "3":
                try:
                    nom_exp = request.POST.get('nom_exp')
                    desc_ex_fi = request.POST.get('desc_ex_fi')
                    soup_fi = request.POST.get('soup_fi')
                    ref_text_leg = request.POST.get('ref_text_leg')
                    
                    try:
                        fiche = FicheInformation.objects.get(id = id)
                        
                        fiche.exploitant_name = nom_exp
                        fiche.infraction_description = desc_ex_fi
                        fiche.soupicious_infraction = soup_fi
                        fiche.ref_legislation_text = ref_text_leg
                    
                        fiche.save()
                        step = "4"

                        context = {'fi_id':fiche.id , "next-step": step}
                        
                    except Exception as e:
                        print(e)
                        context.update({'error':'Impossible de trouver cette fiche'})
                        return HttpResponseBadRequest("Impossible de trouver cette fiche")

                    return JsonResponse(context)

                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")
           
            if step == "4":
                
                try:
                    signature = request.POST.get('signed')

                    fiche = FicheInformation.objects.get(id = id)
                    
                    fiche.sign_obs = signature
                    fiche.date_sign_obs = date.today()
                    fiche.state = "send_to_resp" 

                    fiche.save()
                    context = {'fi_id':fiche.id , "next-step": "5"}
                    return JsonResponse(context)
                    
                    
                except Exception as e:
                    print(e)
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")
        
    
        mode = request.GET.get('mode' , None)

        if mode is None:
            mode = 'view'

        fiche_info = FicheInformation.objects.get(id=id)
        regions = Region.objects.all().order_by('name')
        deps = Department.objects.filter(region = fiche_info.region )
        arrs = Arrondissement.objects.filter(department = fiche_info.department)
        step = 1


        context = {'regions':regions , 'fi':fiche_info , 'mode':mode , 'deps': deps , 'arrs':arrs , "step":step  }

        return render(request , "fiche-info/view_update_fi.html" , context)

    except Exception as e:
        print(e)
        return HttpResponseServerError(e)
    
def validate_fi(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile
        print(request.POST)
        id = request.POST.get("fi_id")
        fiche = FicheInformation.objects.get(id = id)
        signature = request.POST.get('valid-signed')
        
        if fiche.state == "draft":

            fiche.sign_obs = signature
            fiche.date_sign_obs = date.today()
            fiche.state = "send_to_resp" 

        elif fiche.state == "send_to_resp":

            fiche.sign_resp = signature
            fiche.date_sign_resp = date.today()
            fiche.state = "validated_org" 
            fiche.responsable = user_profile

        elif fiche.state == "validated_org":

            fiche.sign_coord = signature
            fiche.date_sign_coord = date.today()
            fiche.state = "validated_coord" 
            fiche.coordinator = user_profile
        
        fiche.save()

        return JsonResponse({"status": "saved"})



def delete_fi(request):
    if request.method == 'POST':
        id = request.POST.get("fi_id")
        fi = FicheInformation.objects.get(id = id)

        fi.delete()

        return JsonResponse({"status": "deleted"})








#####################################################################################
###################################### fiche pertinence stuff #######################
#####################################################################################


@login_required
def fiche_pertinence_registry(request , page):

    user_profile = request.user.userprofile

    if user_profile.role.name_code ==  "coordonnator":
        fiches = FichePertinence.objects.filter( state__in = ["validated_org" , "validated_coord"]).order_by('id').reverse()
    else:
        fiches = FichePertinence.objects.filter(organisation = user_profile.organisation).order_by('id').reverse()

    

    paginator = Paginator(fiches , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    context = {"fiches": page_objects}
    


    return render(request , "fiche-pertinence/registry.html" , context)



@login_required
def create_fiche_pertinence(request , fi_id):

    user_profile = request.user.userprofile

    if request.method == "POST":
        print(request.POST)
        step = request.POST.get("step")
        context = {}
        if step == "1":
            try:
                ref_fi = request.POST.get("ref_fi")
                ref_fp = request.POST.get("ref_fp")
                designation_illegalite = request.POST.get("designation_illegalite")
                denonciateur = request.POST.get("denonciateur")
                domaine = request.POST.get("domaine")
                date_ren = request.POST.get("date_ren")
                
                  
                fiche_info = FicheInformation.objects.get(id=fi_id)
                fiche = FichePertinence.objects.create(ref_fiche = ref_fp , fiche_information = fiche_info, observator = user_profile, organisation = user_profile.organisation, designation = designation_illegalite , domain = domaine , denonciateur  = denonciateur , date_renseignement = datetime.strptime(date_ren, "%d/%m/%Y") , state = 'draft')
                
                request.session['fi_id'] = fiche.id
                step = "2"
                context = {'id_fp':fiche.id , "next-step":step}

                return JsonResponse(context)
            except Exception as e:
                print(e)
                context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")


        if step == "2":
            id_fp = request.POST.get("id_fp" , None)
            contexte = request.POST.get("contexte" , None)
            date_demarage = request.POST.get("date_demarage" , None)
            pertinence = request.POST.get("pertinence" , None)
            priorite = request.POST.get("priorite" , None)
            accesSite = request.POST.get("accesSite" , None)
            encourActivite = request.POST.get("encourActivite" , None)
            arretActivite  = request.POST.get("arretActivite" , None)
            niveau = request.POST.get("niveau" , None)
            niveauSeverite = request.POST.get("niveauSeverite" , None)
            justif = request.POST.get("justif" , None)
            justifNiveauSeverite = request.POST.get("justifNiveauSeverite" , None)

            fiche = FichePertinence.objects.get(id=id_fp)

            fiche.contexte = contexte
            fiche.date_demarage = date_demarage
            
            fiche.priority = priorite
            
            

            if pertinence and int(pertinence) == 1:
                fiche.pertinence = True
                if accesSite and int(accesSite) == 1:
                    fiche.access_site = True
                if encourActivite and int(encourActivite) == 1:
                    fiche.encours_activite = True
                if arretActivite and  int(arretActivite) == 1:
                    fiche.arret_activite = True
                if niveau and int(niveau) == 1:
                    fiche.niveau = True
                if justif and int(justif):

                    fiche.justif = True

                fiche.niveauSeverite = niveauSeverite
                fiche.severity_justif = justifNiveauSeverite
            
            fiche.save()

            step = "3"
            context = {'id_fp':fiche.id , "next-step":step}

            return JsonResponse(context)

        
        if step == "3":
            id_fp = request.POST.get("id_fp")
            fiche = FichePertinence.objects.get(id=id_fp)

            signature = request.POST.get('signed')
            
            fiche.sign_obs = signature
            fiche.date_sign_obs = date.today()
            fiche.state = "send_to_resp" 

            fiche.save()

            step = "4"
            context = {'id_fp':fiche.id , "next-step":step}

            return JsonResponse(context)

            
    ref_fp = 0
    last_id = 1 
    step = 1


    if FichePertinence.objects.last() :
        last_id = FichePertinence.objects.last().id + 1


    if len(str(last_id)) < 2:
        ref_fp = "00"+str(last_id) + "-FP-SNOIE-" + user_profile.organisation.name + "-" + date.strftime(date.today() , "%m%Y")
    else:
        ref_fp = "0"+str(last_id) + "-FP-SNOIE-" + user_profile.organisation.name + "-" + date.strftime(date.today() , "%m%Y")      
        

    try :

        fiche_info = FicheInformation.objects.get(id = fi_id)
    
    except Exception as e:
        return HttpResponseBadRequest("Impossible de trouver cette fiche d'information.")

    context = {"ref_fp" : ref_fp , "organisation": fiche_info.organisation , "step": step ,  "fi_id":fi_id, "fi":fiche_info}

    return render(request , "fiche-pertinence/create_fiche_pertinence.html" , context)

    



@login_required
def view_update_fp(request, id):
    try:

        if request.method == "POST":
            print(request.POST)
            step = request.POST.get("step")
            context = {}
            
            
            
            if step == "1":
                try:
                    
                    step = "2"
                    context = {"next-step":step}

                    return JsonResponse(context)
                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")

            
            if step == "2":
                try:
                    id_fp = request.POST.get("id_fp" , None)
                    contexte = request.POST.get("contexte" , None)
                    date_demarage = request.POST.get("date_demarage" , None)
                    pertinence = request.POST.get("pertinence" , None)
                    priorite = request.POST.get("priorite" , None)
                    accesSite = request.POST.get("accesSite" , None)
                    encourActivite = request.POST.get("encourActivite" , None)
                    arretActivite  = request.POST.get("arretActivite" , None)
                    niveau = request.POST.get("niveau" , None)
                    niveauSeverite = request.POST.get("niveauSeverite" , None)
                    justif = request.POST.get("justif" , None)
                    justifNiveauSeverite = request.POST.get("justifNiveauSeverite" , None)

                    fiche = FichePertinence.objects.get(id=id_fp)

                    fiche.contexte = contexte
                    fiche.date_demarage = date_demarage
                    
                    fiche.priority = priorite
                    
                    

                    if pertinence and int(pertinence) == 1:
                        fiche.pertinence = True
                        if accesSite and int(accesSite) == 1:
                            fiche.access_site = True
                        else:
                            fiche.access_site = False
                        if encourActivite and int(encourActivite) == 1:
                            fiche.encours_activite = True
                        else:
                            fiche.encours_activite = False
                        if arretActivite and  int(arretActivite) == 1:
                            fiche.arret_activite = True
                        else:
                            fiche.arret_activite = False
                        if niveau and int(niveau) == 1:
                            fiche.niveau = True
                        else:
                            fiche.niveau = False
                        if justif and int(justif):
                            fiche.justif = True
                        else:
                            fiche.justif = False

                        fiche.niveauSeverite = niveauSeverite
                        fiche.severity_justif = justifNiveauSeverite

                    else:
                        fiche.pertinence = False
                        fiche.access_site = False
                        fiche.encours_activite = False
                        fiche.arret_activite = False
                        fiche.niveau = False
                        fiche.justif = False
                        fiche.niveauSeverite = False
                        fiche.severity_justif = False
                    
                    fiche.save()

                    step = "3"
                    context = {"next-step":step}

                    return JsonResponse(context)

                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")
            
            if step == "3":
                try:
                    id_fp = request.POST.get("id_fp")
                    fiche = FichePertinence.objects.get(id=id_fp)
                    signature = request.POST.get('signed')

                    fiche.sign_obs = signature
                    fiche.date_sign_obs = date.today()
                    fiche.state = "send_to_resp" 
                    
                    fiche.save()

                    step = "4"
                    context = {'id_fp':fiche.id , "next-step":step}

                    return JsonResponse(context)

                except Exception as e:
                    print(e)
                    context.update({'error':'Une erreur est survenue , merci de contacter votre administrateur'})
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")
           
            if step == "4":
                
                try:
                    signature = request.POST.get('signed')

                    fiche = FicheInformation.objects.get(id = id)
                    
                    fiche.sign_obs = signature
                    fiche.state = "send" 

                    fiche.save()
                    context = {'fi_id':fiche.id , "next-step": "5"}
                    return JsonResponse(context)
                    
                    
                except Exception as e:
                    print(e)
                    return HttpResponseServerError("Une erreur est survenue , merci de contacter votre administrateur")
        
    

        mode = request.GET.get('mode' , None)

        if mode is None:
            mode = 'view'

        fiche_perti = FichePertinence.objects.get(id=id)
        step = 1


        context = {'fp':fiche_perti , 'mode':mode ,  "step":step  }

        return render(request , "fiche-pertinence/view_update_fp.html" , context)

    except Exception as e:
        print(e)
        return HttpResponseServerError(e)


def delete_fp(request):
    if request.method == 'POST':
        id = request.POST.get("fp_id")
        fp = FichePertinence.objects.get(id = id)

        fp.delete()

        return JsonResponse({"status": "deleted"})
    



def validate_fp(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile
        print(request.POST)
        id = request.POST.get("fp_id")
        fiche = FichePertinence.objects.get(id = id)
        signature = request.POST.get('valid-signed')
        
        if fiche.state == "draft":

            fiche.sign_obs = signature
            fiche.date_sign_obs = date.today()
            fiche.state = "send_to_resp" 

        elif fiche.state == "send_to_resp":

            fiche.sign_resp = signature
            fiche.date_sign_resp = date.today()
            fiche.state = "validated_org" 
            fiche.responsable = user_profile

        elif fiche.state == "validated_org":

            fiche.sign_coor = signature
            fiche.date_sign_coo = date.today()
            fiche.state = "validated_coord" 
            fiche.coordinator = user_profile
        
        fiche.save()

        return JsonResponse({"status": "saved"})

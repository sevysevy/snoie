from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView , LogoutView
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, QueryDict
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from UserManagement.models import Organisation, UserProfile , Role

# Create your views here.


class Login(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('alerts-registry' , kwargs={'page': 1},) 
    

    """def form_valid(self, form):
        self.request.session['user_email'] = {"name":self.request.user.email}

        super().form_valid(form)
        #auth_login(self.request, form.get_user())
        #return HttpResponseRedirect(self.get_success_url())
    """
    def form_invalid(self, form):
        messages.error(self.request,'Identifiants invalide')
        return self.render_to_response(self.get_context_data(form=form))
    

class Logout(LogoutView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('index') 
    

    
    



def users_list(request, page):
    user = request.user

    users = UserProfile.objects.filter()

    paginator = Paginator(users , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    orgs = [{"id":elm.id , "name":elm.name} for elm in Organisation.objects.all()]
    roles = [{"id":elm.id , "name":elm.name} for elm in Role.objects.all()]

    context = {"users": page_objects , "orgs": orgs , "roles":roles}

    return render(request , "users/registry.html" , context)




def create_user(request):

    if request.method == "POST":
        lastName = request.POST.get('lastName')
        firstName = request.POST.get('firstName')
        phone = request.POST.get('phone')
        org_id = request.POST.get('organisation')
        role_id = request.POST.get('role')
        email  = request.POST.get('email')
        password = request.POST.get('password')

        organisation = ""
        role = ""

        try:
            organisation = Organisation.objects.get(id = org_id)
            role = Role.objects.get(id = role_id)

            user = User(email = email , first_name=firstName , last_name=lastName , username = email )
            user.set_password(password) 
            user.save()

            userProfile = UserProfile(user = user , firstName = firstName , lastName = lastName , fullName = firstName + " " + lastName , email = email , phone = phone , organisation = organisation , role = role  )

            userProfile.save()
            context = {"id":userProfile.id}

            return JsonResponse(context)
        except Exception as e :
            raise Exception(e)
        
        
    context = {}
    return render(request, "users/create-user.html", context)





def set_session_country(request):

    if request.method =='POST':
        country = request.POST.get("country" , None)
        print(request.POST)

        if country:
            request.session['country'] = country


    return JsonResponse({'msg':country})



def organisations_list(request, page):
    user = request.user

    orgs = Organisation.objects.filter()

    paginator = Paginator(orgs , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    orgs = [{"id":elm.id , "name":elm.name} for elm in Organisation.objects.all()]

    context = {"orgs": page_objects}

    return render(request , "orgs/registry.html" , context)



def roles_list(request, page):
    user = request.user

    roles = Role.objects.filter()

    paginator = Paginator(roles , per_page=15 , orphans=5, allow_empty_first_page=True)

    page_objects = paginator.get_page(page)

    orgs = [{"id":elm.id , "name":elm.name} for elm in Organisation.objects.all()]

    context = {"roles": page_objects}

    return render(request , "roles/registry.html" , context)


def check_email(request):
    email = request.GET.get('email')
    users = UserProfile.objects.all()
    exist = False
    for user in users:
        if user.email == email:
            exist = True
            break

    return JsonResponse({"exist":exist})
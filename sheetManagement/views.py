from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def alert_registry(request):

    user_profile = request.user.userprofile

    context = {}

    return render(request , "alerts/registry.html" , context)
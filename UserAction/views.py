from django.http import JsonResponse
from django.shortcuts import render
from AlertsManagement.models import Alert
from FicheManagement.models import FicheInformation, FichePertinence
from UserAction.models import Comment, UserAction, UserActionType
from mission.models import Mission
from django.template.loader import render_to_string

# Create your views here.


def create_action(name_code , autor , object_id , comment = None):

    action = None

    try: 
        action_type = UserActionType.objects.get(name_code = name_code)

        if(action_type.category == "fi"):
            element = FicheInformation.objects.get(id = object_id)

            action = UserAction.objects.create(action_type = action_type , autor = autor , ficheInformation =element )

        if(action_type.category == "fp"):
            element = FichePertinence.objects.get(id = object_id)

            action = UserAction.objects.create(action_type = action_type , autor = autor , fichePertinence =element )

        if(action_type.category == "alert"):
            element = Alert.objects.get(id = object_id)

            action = UserAction.objects.create(action_type = action_type , autor = autor , alert =element )

        if(action_type.category == "mission"):
            element = Mission.objects.get(id = object_id)

            action = UserAction.objects.create(action_type = action_type , autor = autor , mission =element )
    except Exception as e:
        
        print(e)

        raise Exception(e)
    

    return action



def add_comment(name_code  , object_id, body , autor ):
    comment =""

    try:
        action_type = UserActionType.objects.get(name_code = name_code)

        if(action_type.category == "fi"):
            element = FicheInformation.objects.get(id = object_id)

            #action = UserAction.objects.create(action_type = action_type , autor = autor , ficheInformation =element )

        if(action_type.category == "fp"):
            element = FichePertinence.objects.get(id = object_id)

            #action = UserAction.objects.create(action_type = action_type , autor = autor , fichePertinence =element )

        if(action_type.category == "alert"):
            element = Alert.objects.get(id = object_id)

            action = UserAction.objects.get(action_type = action_type , alert =element )
            comment = Comment.objects.create(body=body , action=action , autor = autor)

        if(action_type.category == "mission"):
            element = Mission.objects.get(id = object_id)

            #action = UserAction.objects.create(action_type = action_type , autor = autor , mission =element )

    except Exception as e:
        print(e)

        raise Exception(e)
    

    return comment




def get_comment_template(request):

    html = render_to_string( "UserAction/add_comment.html")

    return JsonResponse({"html":html})
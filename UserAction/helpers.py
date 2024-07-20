from AlertsManagement.models import Alert
from FicheManagement.models import FicheInformation, FichePertinence
from UserAction.models import UserAction, UserActionType
from mission.models import Mission

# Create your views here.


def create_action(name_code , autor , object_id , comment = None):

    action = None

    try: 
        action_type = UserActionType.get(name_code = name_code)

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


    

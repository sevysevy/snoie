from django.core.management.base import BaseCommand

from UserAction.models import UserActionType

# python manage.py seed --mode=refresh

""" Clear all data and creates  """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

data = [
        {"name":"Creer une fiche d'information" , "name_code":"create-fi" , "cat":"fi"},
        {"name":"Mettre à jours une fiche d'information" , "name_code":"update-fi" , "cat":"fi"},
        {"name":"Valider une fiche d'information et envoyer au responsable" , "name_code":"valider-send-resp-fi" , "cat":"fi"},
        {"name":"Valider une fiche d'information et envoyer à la coordination" , "name_code":"valider-send-coord-fi" , "cat":"fi"},
        {"name":"Supprimer une fiche d'information" , "name_code":"delete-fi" , "cat":"fi"},
        {"name":"Laisser un commentaire sur une fiche d'information" , "name_code":"leave-comment-fi" , "cat":"fi"},

        {"name":"Creer une fiche de pertinence" , "name_code":"create-fp" , "cat":"fp"},
        {"name":"Mettre à jours une fiche de pertinence" , "name_code":"update-fp" , "cat":"fp"},
        {"name":"Valider une fiche de pertinence et envoyer au responsable" , "name_code":"valider-send-resp-fp" , "cat":"fp"},
        {"name":"Valider une fiche de pertinence et envoyer à la coordination" , "name_code":"valider-send-coord-fp" , "cat":"fp"},
        {"name":"Supprimer  une fiche de pertinence" , "name_code":"delete-fp" , "cat":"fp"},
        {"name":"Laisser un commentaire sur une fiche de pertinence" , "name_code":"leave-comment-fp" , "cat":"fp"},


        {"name":"Creer une alerte" , "name_code":"create-alert" , "cat":"alert"},
        {"name":"Mettre à jours une alerte" , "name_code":"update-alert" , "cat":"alert"},
        {"name":"Supprimer une alerte" , "name_code":"delete-alert" , "cat":"alert"},
        {"name":"Laisser un commentaire sur une alerte" , "name_code":"leave-comment-alert" , "cat":"alert"},

        {"name":"Creer une mission" , "name_code":"create-mission" , "cat":"mission"},
        {"name":"Ajouter un document à la mission" , "name_code":"add-doc-to-mission" , "cat":"mission"},
        {"name":"Retirer un document de la mission" , "name_code":"remove-doc-from-mission" , "cat":"mission"},
        {"name":"Annuler une mission" , "name_code":"cancel-mission" , "cat":"mission"},
        {"name":"Terminer une mission" , "name_code":"end-mission" , "cat":"mission"},
        {"name":"Laisser un commentaire sur un document de mission" , "name_code":"leave-comment-mission-doc" , "cat":"mission"},
        {"name":"Supprimer une  mission" , "name_code":"delete-mission" , "cat":"mission"},
        {"name":"Assigner une mission pour Lobbying" , "name_code":"assign-mission-for-lobbying" , "cat":"mission"},
        {"name":"Valider les TDR d'une mission" , "name_code":"validate-tdr-mission" , "cat":"mission"},
        {"name":"Valider le rapport de mission" , "name_code":"validate-mission-report" , "cat":"fp"},
        {"name":"Valider le rapport de mission (CTE)" , "name_code":"validate-mission-report-cte" , "cat":"mission"},
        {"name":"Assigner une mission pour Lobbying" , "name_code":"assign-mission-for-lobbying" , "cat":"mission"},
        {"name":"Charger accusé de reception mission pour Lobbying" , "name_code":"aknowledge-mission-lobbying" , "cat":"mission"},
        
    ]

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete action type instances")
    UserActionType.objects.all().delete()


def create_action_type(elm):

    print("Creating action type")

    

    
    action_type = UserActionType(
        name = elm["name"],
        name_code = elm["name_code"],
        category = elm["cat"]
    )


    action_type.save()
    print("{} action type created.".format(action_type))
    return action_type

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 15 addresses
    for elm in data:
        create_action_type(elm)

from django.urls import path 

from . import views









urlpatterns =[

    path('registry/<int:page>', views.alert_registry, name='alerts-registry'),
    path('create-alert', views.create_alert, name='create-alert'),
    path('view-update-alert/<int:id>', views.view_update_alert, name='view-update-alert'),
    path('delete-alert', views.delete_alert, name='delete-alert'),
    path('get-alert-info/<int:id>', views.get_alert_info, name='get-alert-info'),
    
]
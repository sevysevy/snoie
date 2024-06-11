from django.urls import path 

from . import views









urlpatterns =[

    path('fiche-info-registry/<int:page>', views.fiche_info_registry, name='fiche-info-registry'),
    path('create-fiche-info', views.create_fiche_info, name='create-fiche-info'),
    path('fiche-pertinence-registry/<int:page>', views.fiche_pertinence_registry, name='fiche-pertinence-registry'),
    path('get-fiches-info', views.get_fiches_info, name='get-fiches-info'),
    path('create-fiche-pertinence/<int:fi_id>', views.create_fiche_pertinence, name='create-fiche-pertinence'),
    path('view-update-fiche-info/<int:id>', views.view_update_fi, name='view-update-fi'),
    path('view-update-fiche-pertinence/<int:id>', views.view_update_fp, name='view-update-fp'),
    path('delete-fiche-info', views.delete_fi, name='delete-fi'),
    path('delete-fiche-pertinence', views.delete_fp, name='delete-fp'),
    path('sign-validate-fiche-info', views.validate_fi, name='sign-validate-fi'),
    path('sign-validate-fiche-pertinence', views.validate_fp, name='sign-validate-fp'),
] 
from django.urls import path 

from . import views



urlpatterns =[

    path('stat-al', views.statistic_alert, name='stat-alert'),

    path('stat-fi', views.statistic_fiche, name='stat-fiche'),
    
    path('stat-mis', views.statistic_mission, name='stat-mission'),

    path('stat-al-datas' , views.statistic_alert_datas, name="stat-al-datas"),

    path('stat-fi-fp-datas' , views.statistic_fiche_datas, name="stat-fi-fp-datas"),

    path('stat-mi-datas' , views.statistic_mission_datas, name="stat-mi-datas")
    
] 
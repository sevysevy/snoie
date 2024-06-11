from django.urls import path 

from . import views



urlpatterns =[

    path('registry/<int:page>', views.mission_registry, name='mission-registry'),
    path('create-mission', views.create_mission, name='create-mission'),
    path('detail-mission/<int:id>', views.detail_mission, name='detail-mission'),
    
] 
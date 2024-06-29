from django.urls import path 

from . import views



urlpatterns =[

    path('registry/<int:page>', views.mission_registry, name='mission-registry'),
    path('create-mission', views.create_mission, name='create-mission'),
    path('detail-mission/<int:id>', views.detail_mission, name='detail-mission'),
    path('download-mission-doc/<int:id>', views.download_mission_doc, name='download-mission-doc'),
    path('add-mission-doc/<int:id>', views.add_mission_doc, name='add-mission-doc'),
    path('start-mission/<int:id>', views.start_mission, name='start-mission'),
    
] 
from django.urls import path 

from . import views









urlpatterns =[

    path('lobby-registry/<int:page>', views.lobby_registry, name='lobby-registry'),
    path('lobby-details/<int:id>', views.lobby_details, name='lobby-details'),
] 
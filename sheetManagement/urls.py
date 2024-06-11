
from django.urls import path 

from . import views




urlpatterns =[

    path('information-sheet', views.information_sheet, name='information-sheet'),
    path('relevance-sheet', views.relevance_sheet, name='relevance-sheet'),
    
]
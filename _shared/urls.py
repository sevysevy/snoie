
from django.urls import path 

from . import views




urlpatterns =[

    path('get-departments', views.get_departments, name='get-departments'),
    path('get-arr', views.get_arr, name='get-arr'),
    
]
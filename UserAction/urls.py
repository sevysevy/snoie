from django.urls import path , include

from . import views




urlpatterns =[

    path('get-comment-template', views.get_comment_template, name='get-comment-template'),
]
from django.contrib.auth import views as auth_views 
from django.urls import path , include
from allauth.account.views import PasswordResetView

from . import views




urlpatterns =[

    path('login', views.Login.as_view(redirect_authenticated_user = True) , name='login'),
    path('logout', views.Logout.as_view() , name='logout'),
    path('check-email', views.check_email , name='check-email'),
    path('users/<int:page>', views.users_list , name='users-list'),
    path('create-user', views.create_user , name='create-user'),
    path('set-session-country', views.set_session_country , name='set-session-country'),

    path('organisations/<int:page>', views.organisations_list , name='organisations-list'),

    path('roles/<int:page>', views.roles_list , name='roles-list'),
    

]


#path("password/reset/", PasswordResetView.as_view(), name="account_reset_password"),

    #path('signup/', views.register, name='signup'),
    #path('first-login/<email>', views.first_login, name='first_login'),
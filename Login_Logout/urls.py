from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
  
  path('Register/', views.Register, name = 'Registerpage'),
  path('Login/', views.simple_user_login, name ='simple_user_login'),
  path('Author-Login/', views.Custom_admin_login, name ='Custom_admin_login'),
  path('Logout/', views.LogoutView, name ='logoutview'),
  path('Edit-User-data/', views.Edit_user_data, name ='Edit_user_data'),
  
  
 
]

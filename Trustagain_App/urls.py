from django.contrib import admin
from django.urls import path, include
from Trustagain_App import views

urlpatterns = [
    path('', views.users, name='users'), 
    
]
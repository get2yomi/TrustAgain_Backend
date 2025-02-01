from django.contrib import admin
from django.urls import path, include
from Trustagain_App import views
from .views import RegisterView, LoginView, InputDataView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('submit-data/', InputDataView.as_view(), name='submit_data'),
]

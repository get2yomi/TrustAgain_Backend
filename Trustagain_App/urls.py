from django.contrib import admin
from django.urls import path, include
from Trustagain_App import views
from django.urls import path
from Trustagain_App.views import (
    RegisterView, LoginView, InputDataView, create_shift_narrative,
    TimeSheetView, create_time_sheet, list_time_sheets, update_time_sheet, delete_time_sheet,
    create_incident_report, list_incident_reports, update_incident_report, delete_incident_report
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('submit-data/', InputDataView.as_view(), name='submit_data'),
    path('api/shift-narrative/', create_shift_narrative, name='create_shift_narrative'),
    path("time-sheet/", TimeSheetView.as_view(), name="time-sheet"),
    path('api/time-sheet/', create_time_sheet, name='create_time_sheet'),
    path('api/time-sheet/list/', list_time_sheets, name='list_time_sheets'),
    path('api/time-sheet/update/<int:pk>/', update_time_sheet, name='update_time_sheet'),
    path('api/time-sheet/delete/<int:pk>/', delete_time_sheet, name='delete_time_sheet'),
    
    # Incident Report URLs
    path('api/incident-report/', create_incident_report, name='create_incident_report'),
    path('api/incident-report/list/', list_incident_reports, name='list_incident_reports'),
    path('api/incident-report/update/<int:pk>/', update_incident_report, name='update_incident_report'),  # ✅ Fixed syntax error
    path('api/incident-report/delete/<int:pk>/', delete_incident_report, name='delete_incident_report'),
]

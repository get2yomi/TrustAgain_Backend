from django.urls import path
from Trustagain_App.views import (
    RegisterView, LoginView, InputDataView, create_shift_narrative,
    TimeSheetView, create_time_sheet, list_time_sheets, update_time_sheet, delete_time_sheet,
    create_incident_report, list_incident_reports, update_incident_report, delete_incident_report
)
from .views import get_unfinished_forms
from .views import ShiftNarrativeView
from .views import get_shift_narrative
from . import views
from .views import incident_report_view




urlpatterns = [
    # ✅ FIX: Ensure all API routes start with "api/"
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('submit-data/', InputDataView.as_view(), name='submit_data'),
    path('shift-narrative/create/', create_shift_narrative, name='create_shift_narrative'),
    path('shift-narrative/', ShiftNarrativeView.as_view(), name='shift-narrative'),
    path("timesheet/", TimeSheetView.as_view(), name="timesheet"),
    
    # Time Sheet URLs
    path('time-sheet/create/', create_time_sheet, name='create_time_sheet'),
    path('time-sheet/list/', list_time_sheets, name='list_time_sheets'),
    path('time-sheet/update/<int:pk>/', update_time_sheet, name='update_time_sheet'),
    path('time-sheet/delete/<int:pk>/', delete_time_sheet, name='delete_time_sheet'),
    
    # Incident Report URLs
    path('incident-report/create/', create_incident_report, name='create_incident_report'),
    path('incident-report/list/', list_incident_reports, name='list_incident_reports'),
    path('incident-report/update/<int:pk>/', update_incident_report, name='update_incident_report'),
    path('incident-report/delete/<int:pk>/', delete_incident_report, name='delete_incident_report'),
    
    # Unfinished Forms
    #path('api/get-unfinished-forms/', get_unfinished_forms, name='get_unfinished_forms'),
    # path('login/', views.login_view, name='login'),
    # path('index/', views.index_view, name='index'),


    path('api/shift-narrative/', get_shift_narrative, name='shift_narrative'),
  
   path('home/', views.homepage_view, name='homepage'),  # Redirected homepage
   path('logout/', views.logout_view, name='logout'),
    path('incident-report/', views.incident_report_view, name='incident_report'),
    path('shift-narrative/', views.shift_narrative_view, name='shift_narrative'),
    path('timesheet/', views.timesheet_view, name='timesheet'),
   path('incident-report/', incident_report_view, name='incident_report'),

    # path('', views.index_view, name='index'),  # 👈 this handles http://127.0.0.1:8000/

    # path('', views.login_view, name='login'),          # Login page

]

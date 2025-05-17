from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import InputData, ShiftNarrative, TimeSheet, IncidentReport
from .serializers import UserSerializer, InputDataSerializer, ShiftNarrativeSerializer, TimeSheetSerializer, IncidentReportSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .models import UnfinishedForm
from django.contrib.auth.models import User  # Ensure correct user handling
from rest_framework.permissions import IsAuthenticated
from .serializers import ShiftNarrativeSerializer
from .models import ShiftNarrative
from rest_framework import status
import logging
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from .models import IncidentReport, ShiftNarrative, TimeSheet  # adjust to your models

logger = logging.getLogger(__name__)

# Get user model dynamically
User = get_user_model()

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # ⬅️ Make sure this matches your URLs
        else:
            return render(request, 'Trust_App/login.html', {'error': 'Invalid credentials'})

    return render(request, 'Trust_App/login.html')

# User Registration
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]  # ✅ Allow anyone to log in

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # ✅ Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# API to accept screen input data
class InputDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.data['user'] = request.user.id  # Attach user ID
        serializer = InputDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to create a time sheet entry
class TimeSheetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        received_data = request.data.copy()  # Store received data
        received_data["user"] = request.user.id  # Attach logged-in user
        
        logger.info(f"Received TimeSheet Data: {received_data}")  # ✅ Log received data

        serializer = TimeSheetSerializer(data=received_data)
        if serializer.is_valid():
            saved_data = serializer.save()
            logger.info("Time sheet submitted successfully.")  # ✅ Log success
            return Response(
                {
                    "message": "Time sheet submitted successfully",
                    "captured_data": received_data,
                    "saved_data": serializer.data,
                }, 
                status=status.HTTP_201_CREATED
            )
        
        logger.error(f"TimeSheet Validation Errors: {serializer.errors}")  # ✅ Log errors
        return Response(
            {
                "message": "Time sheet submission failed",
                "captured_data": received_data,
                "errors": serializer.errors,
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )



# ///-------------------------------///

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_time_sheet(request):
    serializer = TimeSheetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Assign logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_time_sheets(request):
    time_sheets = TimeSheet.objects.filter(user=request.user)  # Filter by logged-in user
    serializer = TimeSheetSerializer(time_sheets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_time_sheet(request, pk):
    try:
        time_sheet = TimeSheet.objects.get(pk=pk, user=request.user)
    except TimeSheet.DoesNotExist:
        return Response({"error": "Time sheet not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TimeSheetSerializer(time_sheet, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_time_sheet(request, pk):
    try:
        time_sheet = TimeSheet.objects.get(pk=pk, user=request.user)
    except TimeSheet.DoesNotExist:
        return Response({"error": "Time sheet not found"}, status=status.HTTP_404_NOT_FOUND)

    time_sheet.delete()
    return Response({"message": "Time sheet deleted"}, status=status.HTTP_204_NO_CONTENT)


# List Incident Reports for Logged-in User
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_incident_reports(request):
    reports = IncidentReport.objects.filter(user=request.user)  # Filter by logged-in user
    serializer = IncidentReportSerializer(reports, many=True)
    return Response(serializer.data)

# Update Incident Report
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_incident_report(request, pk):
    try:
        report = IncidentReport.objects.get(pk=pk, user=request.user)
    except IncidentReport.DoesNotExist:
        return Response({"error": "Incident report not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = IncidentReportSerializer(report, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Incident Report
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_incident_report(request, pk):
    try:
        report = IncidentReport.objects.get(pk=pk, user=request.user)
    except IncidentReport.DoesNotExist:
        return Response({"error": "Incident report not found"}, status=status.HTTP_404_NOT_FOUND)

    report.delete()
    return Response({"message": "Incident report deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_incident_report(request):
    print("Authenticated User:", request.user)  # ✅ Debugging step

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    # ✅ Create a copy of request.data instead of modifying it directly
    data = request.data.copy()
    data['user'] = request.user.id  # Attach the logged-in user ID

    serializer = IncidentReportSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_time_sheet(request):
    print("Received Data from React Native:", request.data)  # ✅ See the exact data received

    # ✅ Attach user to the request data (if TimeSheet is linked to a user)
    data_with_user = request.data.copy()
    data_with_user['user'] = request.user.id

    serializer = TimeSheetSerializer(data=data_with_user)

    if serializer.is_valid():
        serializer.save()
        print("Data Successfully Saved!")  # ✅ Confirm successful save
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    print("Validation Errors:", serializer.errors)  # ✅ Show validation errors if any
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def get_unfinished_forms(request):
    username = request.GET.get('username')  # Get the username from request
    if not username:
        return JsonResponse({"error": "Username is required"}, status=400)

    # Filter for unfinished forms linked to the given username
    forms = UnfinishedForm.objects.filter(username=username, submitted=False)

    if forms.exists():
        form_data = [{"type": form.form_type, "id": form.id} for form in forms]
        return JsonResponse({"unfinished_forms": form_data})
    
    return JsonResponse({"unfinished_forms": []})  # Return empty if no pending forms

# shift narrative 
class ShiftNarrativeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ShiftNarrativeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Link narrative to the user
            return Response({"message": "Shift narrative saved successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    # ✅ Shift Narrative API (Fixed User & Time Formatting)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_shift_narrative(request):
    data = request.data.copy()
    data['user'] = request.user.id  # ✅ Ensure user is attached

    # ✅ Convert time format before saving
    try:
        if 'Time_in' in data:
            data['Time_in'] = datetime.strptime(data['Time_in'], "%H:%M:%S").time()
        if 'Time_out' in data:
            data['Time_out'] = datetime.strptime(data['Time_out'], "%H:%M:%S").time()
    except ValueError:
        return Response({"error": "Invalid time format error. Use HH:MM:SS"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ShiftNarrativeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Shift narrative submitted successfully",
            "captured_data": data,
            "saved_data": serializer.data,
        }, status=status.HTTP_201_CREATED)

    return Response({"message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def get_shift_narrative(request):
    data = {
        "status": "success",
        "message": "Shift narrative data fetched successfully",
        "data": {
            "id": 1,
            "shift_name": "Night Shift",
            "description": "Incident reported at midnight",
            "timestamp": "2025-03-18T12:00:00Z"
        }
    }



def index_view(request):
    return render(request, 'Trust_App/index.html')  # This matches your folder

# html start from here


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to homepage after login
        else:
            return render(request, 'Trust_App/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'Trust_App/login.html')

# Homepage view (after login)
@login_required
def homepage_view(request):
    return render(request, 'Trust_App/homepage.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')




def dashboard_view(request):
    return render(request, 'Trust_App/homepage.html')  # your dashboard file

def incident_report_view(request):
    reports = IncidentReport.objects.all()
    return render(request, 'Trust_App/incident_report.html', {'incident_reports': reports})

def shift_narrative_view(request):
    shifts = ShiftNarrative.objects.all()
    return render(request, 'Trust_App/shift_narrative.html', {'shift_narratives': shifts})

def timesheet_view(request):
    sheets = TimeSheet.objects.all()
    return render(request, 'Trust_App/timesheet.html', {'timesheets': sheets})



def incident_report_view(request):
    reports = IncidentReport.objects.all()
    return render(request, 'Trust_App/incident_report.html', {'reports': reports})


    return Response(data)

def duration_hours(self):
    try:
        if self.date_in and self.time_in and self.time_out:
            in_time = datetime.datetime.combine(self.date_in, self.time_in)
            # If date_out is not set, assume same day unless time_out < time_in (overnight)
            if self.date_out:
                out_time = datetime.datetime.combine(self.date_out, self.time_out)
            else:
                out_time = datetime.datetime.combine(self.date_in, self.time_out)
                if self.time_out < self.time_in:
                    out_time += datetime.timedelta(days=1)
            return round((out_time - in_time).total_seconds() / 3600, 2)
    except Exception as e:
        print(f"Error calculating duration: {e}")
    return 0

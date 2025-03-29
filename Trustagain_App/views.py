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



# Get user model dynamically
User = get_user_model()

def index(request):
    return HttpResponse("form_page.html")  # Corrected HttpResponse usage

# User Registration
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login (returns JWT token)
# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if username:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             })
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ FIXED: Proper class-based view for login
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

# # API to create a shift narrative
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])  # Ensure authentication
# def create_shift_narrative(request):
#     serializer = ShiftNarrativeSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # API to create a time sheet entry
# class TimeSheetView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         print("Received Data:", request.data)  # ✅ Debug log
#         data = request.data.copy()
#         data["user"] = request.user.id  # Attach logged-in user

#         serializer = TimeSheetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Time sheet submitted successfully"}, status=status.HTTP_201_CREATED)
#         print("Validation Errors:", serializer.errors)  # ✅ Debug errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # --------------------------


# # Configure logging
# logger = logging.getLogger(__name__)

# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])  # Ensure authentication
# def create_shift_narrative(request):
#     received_data = request.data  # Store received data
#     logger.info(f"Received Shift Narrative Data: {received_data}")  # ✅ Log received data

#     serializer = ShiftNarrativeSerializer(data=received_data)
#     if serializer.is_valid():
#         saved_data = serializer.save()
#         logger.info("Shift narrative saved successfully.")  # ✅ Log success
#         return Response(
#             {
#                 "message": "Shift narrative submitted successfully",
#                 "captured_data": received_data,
#                 "saved_data": serializer.data,
#             }, 
#             status=status.HTTP_201_CREATED
#         )
    
#     logger.error(f"Shift Narrative Validation Errors: {serializer.errors}")  # ✅ Log errors
#     return Response(
#         {
#             "message": "Shift narrative submission failed",
#             "captured_data": received_data,
#             "errors": serializer.errors,
#         }, 
#         status=status.HTTP_400_BAD_REQUEST
#     )

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
    return Response(data)

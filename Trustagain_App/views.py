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

# API to create a shift narrative
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # Ensure authentication
def create_shift_narrative(request):
    serializer = ShiftNarrativeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to create a time sheet entry
class TimeSheetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("Received Data:", request.data)  # ✅ Debug log
        data = request.data.copy()
        data["user"] = request.user.id  # Attach logged-in user

        serializer = TimeSheetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Time sheet submitted successfully"}, status=status.HTTP_201_CREATED)
        print("Validation Errors:", serializer.errors)  # ✅ Debug errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    request.data['user'] = request.user.id  # Attach the logged-in user ID
    serializer = IncidentReportSerializer(data=request.data)
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

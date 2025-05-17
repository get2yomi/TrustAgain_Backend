from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import InputData
from .models import ShiftNarrative
from .models import TimeSheet
from .models import IncidentReport
from django import forms

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Input Data Serializer
class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputData
        fields = '__all__'


class ShiftNarrativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftNarrative
        fields = '__all__'

class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = '__all__'

class IncidentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = '__all__'

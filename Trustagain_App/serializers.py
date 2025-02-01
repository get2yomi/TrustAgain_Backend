from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import InputData

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

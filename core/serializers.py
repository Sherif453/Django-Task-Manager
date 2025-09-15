from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
import pytz

class TaskSerializer(serializers.ModelSerializer):
    """
    ModelSerializer: DRF reads your Django model and auto-builds fields.
    It handles validation, (de)serialization, and saving.
    """
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    
    def validate_due_date(self, value):
        from datetime import date, datetime
        if value:
            today = datetime.combine(date.today(), datetime.min.time(), tzinfo=pytz.UTC)
            if value < today:
                raise serializers.ValidationError("Due date cannot be in the past.")
        return value

class RegisterSerializer(serializers.ModelSerializer):
    password =  serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  #redundant
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

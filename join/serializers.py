from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers
from .models import Task

class SiginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','password', 'email']

    def create(self, validated_data):
        # Benutzer mit dem übergebenen Passwort erstellen
        try:
            user = User.objects.create_user(
                username=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                email=validated_data['email']
            )
            return user
        except IntegrityError:
            # Fange IntegrityError ab und gebe eine ValidationError zurück
            raise serializers.ValidationError({"Email already exists!"})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email'] 

class TaskSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()  # Um den Namen der Kategorie anzuzeigen
    # assigned_users = serializers.StringRelatedField(many=True)  # Um die Namen der User anzuzeigen
    # assigned_users = UserSerializer(many=True) 
    due_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'assigned_users'] #  'category'
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken, Token, Response 
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import SiginUserSerializer, CategorySerializer, TaskSerializer
from .models import Task, Category
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Token des aktuellen Benutzers abrufen
            token = request.auth
            # Token löschen
            token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # Erfolgreiches Logout
        except Token.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Token nicht gefunden

class SiginUserView(APIView):
    def post(self, request):
        serializer = SiginUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Stellt sicher, dass der User authentifiziert ist

    def get(self, request):
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data)     

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if pk in [1, 2, 3]:
            return Response({'detail': 'Not allowed to delete this category.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # Erfolgreiches Löschen ohne Inhalt
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # Category nicht gefunden
        

class TaskViewSet(APIView):
    # serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Stellt sicher, dass der User authentifiziert ist

    def get(self, request):
        tasks = Task.objects.all()  #filter(assigned_users=self.request.user) # Um zu filtern was nur einem selbst zugewisen ist!
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)     
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # `author` automatisch auf den eingeloggten Benutzer setzen
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, author=request.user)  # Nur löschen, wenn der Benutzer der Autor ist
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # Erfolgreiches Löschen ohne Inhalt
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # Task nicht gefunden
    
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, author=request.user)  # Überprüfen, ob der Benutzer der Autor ist
            serializer = TaskSerializer(task, data=request.data)  # Bestehende Aufgabe laden und neue Daten bereitstellen
            if serializer.is_valid():
                serializer.save()  # Aufgabe aktualisieren
                return Response(serializer.data, status=status.HTTP_200_OK)  # Erfolgreiche Aktualisierung
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Fehler bei Validierung
        except Task.DoesNotExist:
            print(f"Task with id {pk} does not exist or is not authored by {request.user.id}")
            return Response(status=status.HTTP_404_NOT_FOUND)  # Aufgabe nicht gefunden
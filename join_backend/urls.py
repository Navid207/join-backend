from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from join.views import LoginView, LogoutView, SiginUserView, TaskViewSet, CategoryView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()), 
    path('register/', SiginUserView.as_view(), name='user-registration'),
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>/', CategoryView.as_view()),
    path('tasks/', TaskViewSet.as_view()),
    path('tasks/<int:pk>/', TaskViewSet.as_view()),  # Hier wird `pk` für die ID verwendet
]

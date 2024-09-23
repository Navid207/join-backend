from turtle import color
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User


# Erstelle eine Funktion, um die Standardkategorie zu bekommen
def get_default_category():
    try:
        return Category.objects.get(name="Backend")
    except ObjectDoesNotExist:
        return None  # Fallback, falls die Kategorie nicht existiert

class Category(models.Model):
    name = models.CharField(max_length=100, default= "Backend")
    color_code = models.CharField(max_length=100, default="#FFFFFF")
    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, '1-low'),
        (2, '2-medium'),
        (3, '3-urgent'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.IntegerField( 
        choices=PRIORITY_CHOICES,  # Nur Werte 1, 2, oder 3 sind erlaubt
        default=1
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_tasks'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        default=get_default_category # lambda: Category.objects.get(name="Backend")
        )
    assigned_users = models.ManyToManyField(
        User,
        related_name='assigned_tasks'
        )

    def __str__(self):
        return self.title

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

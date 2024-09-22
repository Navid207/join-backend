from turtle import color
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=50)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_tasks'
    )
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    assigned_users = models.ManyToManyField(
        User,
        related_name='assigned_tasks'
        )

    def __str__(self):
        return self.title


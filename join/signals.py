from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    # Standardkategorien, die immer vorhanden sein sollen
    default_categories = [
        {'name': 'Backend', 'color_code': '#FF0000'},
        {'name': 'Frontend', 'color_code': '#00FF00'},
        {'name': 'DevOps', 'color_code': '#0000FF'},
    ]

    for category_data in default_categories:
        # Kategorie nur hinzufügen, wenn sie nicht bereits existiert
        Category.objects.get_or_create(name=category_data['name'], defaults=category_data)

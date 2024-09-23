from django.apps import AppConfig


class JoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'join'

    def ready(self):
        import join.signals  # Hier das Signal importieren
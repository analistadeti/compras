from django.apps import AppConfig


class ComprasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compras'

class ComprasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compras'

    def ready(self):
        import compras.signals  # Importar las señales aquí

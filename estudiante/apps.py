from django.apps import AppConfig

class EstudianteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estudiante' # En minúscula y singular

    def ready(self):
        import estudiante.signals

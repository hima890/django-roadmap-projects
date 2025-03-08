from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        """
        This method is called when the Django application is ready.
        It imports the signals module to ensure that signal handlers
        are connected when the application starts.
        """
        
        import user.signals

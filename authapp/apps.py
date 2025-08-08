from django.apps import AppConfig

class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'
    verbose_name = '用户认证'

    def ready(self):
        import authapp.signals

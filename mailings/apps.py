from django.apps import AppConfig


class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'

    """ 
    Привязываем сигналы к нашему приложению
    """
    def ready(self):
        import mailings.signals
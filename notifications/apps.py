from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        from . import handlers
        from . import signals
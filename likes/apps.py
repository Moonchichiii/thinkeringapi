from django.apps import AppConfig

class LikesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'likes'

    def ready(self):
        from notifications.handlers import create_notification_for_like_handler
        from notifications.signals import create_notification_for_like
        create_notification_for_like.connect(create_notification_for_like_handler)

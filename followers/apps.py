from django.apps import AppConfig

class FollowersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'followers'

    def ready(self):
        from notifications.handlers import create_notification_for_follow_handler
        from notifications.signals import create_notification_for_follow
        create_notification_for_follow.connect(create_notification_for_follow_handler)

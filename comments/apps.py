from django.apps import AppConfig

class CommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'

    def ready(self):
        from notifications.handlers import create_notification_for_comment_handler
        from notifications.signals import create_notification_for_comment
        create_notification_for_comment.connect(create_notification_for_comment_handler)

from django.dispatch import Signal

# Define custom signals
create_notification_for_comment = Signal()
create_notification_for_like = Signal()
create_notification_for_follow = Signal()

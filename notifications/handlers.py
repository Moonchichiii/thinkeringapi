from django.dispatch import receiver
from .signals import create_notification_for_comment, create_notification_for_follow, create_notification_for_like
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.cache import cache
from django.apps import apps
from datetime import timedelta

# Constants
RATE_LIMIT_KEY = "notification_rate_limit:{user_id}"
RATE_LIMIT = 10  
BATCH_TIMEFRAME = timedelta(minutes=5)
NOTIFICATION_MESSAGES = {
    'follow': 'started following you.',
    'like': 'liked your post.',
    'comment': 'commented on your post.',
    'reply': 'replied to your comment.'
}

@receiver(create_notification_for_like)
def create_notification_for_like_handler(sender, instance, **kwargs):
    Notification = apps.get_model('notifications', 'Notification')
    rate_limit_key = RATE_LIMIT_KEY.format(user_id=instance.profile.user.id)
    count = cache.get(rate_limit_key, 0)

    if count >= RATE_LIMIT:
        return  

    cache.incr(rate_limit_key)
    cache.expire(rate_limit_key, 3600)  

    existing_notification = Notification.objects.filter(
        recipient=instance.post.author,
        actor=instance.profile,
        verb=NOTIFICATION_MESSAGES['like'],
        target=instance.post,
        created_at__gte=timezone.now() - BATCH_TIMEFRAME
    ).first()

    if existing_notification:
        existing_notification.batch_count += 1
        existing_notification.last_aggregated = timezone.now()
        existing_notification.save()
    else:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.profile,
            verb=NOTIFICATION_MESSAGES['like'],
            target=instance.post,
            action_object=instance
        )

@receiver(create_notification_for_comment)
def create_notification_for_comment_handler(sender, instance, **kwargs):
    Notification = apps.get_model('notifications', 'Notification')
    verb = 'reply' if instance.parent else 'comment'
    recipient = instance.parent.author if instance.parent else instance.post.author
    if recipient != instance.author: 
        Notification.objects.create(
            recipient=recipient,
            actor=instance.author,
            verb=NOTIFICATION_MESSAGES[verb],
            target=instance.post,
            action_object=instance
        )

@receiver(create_notification_for_follow)
def create_notification_for_follow_handler(sender, instance, **kwargs):
    Notification = apps.get_model('notifications', 'Notification')
    Notification.objects.create(
        recipient=instance.followed,
        actor=instance.follower,
        verb=NOTIFICATION_MESSAGES['follow'],
        target_content_type=ContentType.objects.get_for_model(instance.followed),
        target_object_id=instance.followed.id,
        action_object_content_type=ContentType.objects.get_for_model(instance),
        action_object_id=instance.id
    )

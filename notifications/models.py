from django.db import models
from profiles.models import Profile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
    )

    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    action_object_content_type = models.ForeignKey(ContentType, related_name='action_object', on_delete=models.CASCADE)
    action_object_id = models.PositiveIntegerField()
    action_object = GenericForeignKey('action_object_content_type', 'action_object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    batch_count = models.PositiveIntegerField(default=1)
    last_aggregated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification: {self.actor} {self.verb} {self.target} {self.created_at}'

from rest_framework import serializers
from profiles.serializers import ProfileSerializer
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = ProfileSerializer(read_only=True)
    recipient = ProfileSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'action_object', 'created_at', 'read', 'batch_count', 'last_aggregated']
        read_only_fields = ['recipient', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.batch_count > 1:
            data['message'] = f"{instance.actor.user.username} and {instance.batch_count - 1} others {instance.verb}"
        else:
            data['message'] = f"{instance.actor.user.username} {instance.verb}"
        return data

from rest_framework import serializers
from profiles.models import Profile
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'profile', 'post', 'created_at']
        read_only_fields = ['profile', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user and not attrs.get('profile'):
            attrs['profile'] = Profile.objects.get(user=request.user)
        return super().validate(attrs)

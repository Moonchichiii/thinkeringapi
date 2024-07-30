from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'profile', 'post', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['profile']

    def validate(self, attrs):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user') and not attrs.get('profile'):
            attrs['profile'] = request.user.profile
        if Rating.objects.filter(profile=attrs.get('profile'), post=attrs.get('post')).exists():
            raise serializers.ValidationError("You have already rated this post.")
        return super().validate(attrs)

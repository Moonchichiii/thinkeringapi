from rest_framework import serializers
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileSerializer(read_only=True)
    followed = ProfileSerializer(read_only=True)
    follow_duration = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at', 'follow_duration']

    def get_follow_duration(self, obj):
        return obj.follow_duration

class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['followed']

    def validate_followed(self, value):
        request = self.context.get('request')
        if not Profile.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Profile does not exist.")
        if request and request.user.profile == value:
            raise serializers.ValidationError("You cannot follow yourself.")
        return value

    def create(self, validated_data):
        follower = self.context['request'].user.profile
        followed = validated_data['followed']
        return Follow.objects.create(follower=follower, followed=followed)

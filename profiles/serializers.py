from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    avatar_url = serializers.SerializerMethodField()
    post_count = serializers.IntegerField(source='post_count', read_only=True)

    class Meta:
        model = Profile
        fields = ['bio', 'avatar_url', 'username', 'followers_count', 'following_count', 'post_count']
        read_only_fields = ['username', 'followers_count', 'following_count', 'post_count']

    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None


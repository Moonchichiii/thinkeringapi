from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    post_count = serializers.IntegerField(read_only=True)
    is_popular = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['bio', 'avatar_url', 'username', 'followers_count', 'following_count', 'post_count', 'is_popular']
        read_only_fields = ['username', 'followers_count', 'following_count', 'post_count', 'is_popular']

    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    def get_followers_count(self, obj):
        return obj.followers_count()

    def get_following_count(self, obj):
        return obj.following_count()

    def get_is_popular(self, obj):
        return obj.is_popular

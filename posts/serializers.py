from rest_framework import serializers
from .models import Post
from profiles.serializers import ProfileSerializer

class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    post_count = serializers.IntegerField(source='author.post_count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'image', 'created_at', 'updated_at', 'approved', 'average_rating', 'rating_count', 'likes_count', 'post_count']

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image file size must be less than 2MB.")
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            raise serializers.ValidationError("Image file must be in PNG, JPG, JPEG, or WEBP format.")
        return value

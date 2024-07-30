from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at', 'parent']
        read_only_fields = ['author', 'created_at', 'updated_at']

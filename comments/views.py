from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Comment
from .serializers import CommentSerializer
from backend.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from profiles.models import Profile

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author']

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        try:
            serializer.save(author=profile)
        except Exception as e:
            # Provide a cleaner message for the frontend
            raise ValidationError({"detail": "Failed to create comment. Please try again later."})

    def perform_update(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        try:
            serializer.save(author=profile)
        except Exception as e:
            # Provide a cleaner message for the frontend
            raise ValidationError({"detail": "Failed to update comment. Please try again later."})

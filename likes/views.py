from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Like
from .serializers import LikeSerializer
from profiles.models import Profile

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().select_related('profile', 'post')
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post', 'profile']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        post = serializer.validated_data.get('post')
        profile = Profile.objects.get(user=self.request.user)
        if post.author == profile:
            raise IntegrityError("You cannot like your own post.")
        if Like.objects.filter(profile=profile, post=post).exists():
            raise IntegrityError("You have already liked this post.")
        serializer.save(profile=profile)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from .models import Follow
from .serializers import FollowSerializer, FollowCreateSerializer
from profiles.models import Profile
from backend.pagination import StandardResultsSetPagination

# Create your views here.

class FollowListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user.profile)

    def get_serializer_class(self):
        return FollowCreateSerializer if self.request.method == 'POST' else FollowSerializer

    def perform_create(self, serializer):
        followed_profile = serializer.validated_data['followed']
        if not Profile.objects.filter(pk=followed_profile.id).exists():
            raise NotFound({"detail": "Profile not found."})
        if followed_profile == self.request.user.profile:
            raise ValidationError({"detail": "You cannot follow yourself."})
        if Follow.objects.filter(follower=self.request.user.profile, followed=followed_profile).exists():
            raise ValidationError({"detail": "You are already following this profile."})
        serializer.save(follower=self.request.user.profile)


class FollowDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_object(self):
        followed_id = self.kwargs['pk']
        followed = get_object_or_404(Profile, pk=followed_id)
        return get_object_or_404(Follow, follower=self.request.user.profile, followed=followed)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)

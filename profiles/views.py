from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from django.apps import apps

# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def follow_stats(self, request):
        profile = request.user.profile
        followers_count = profile.followers_count()
        following_count = profile.following_count()
        return Response({
            'followers_count': followers_count,
            'following_count': following_count
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        profile_to_follow = self.get_object()
        if profile_to_follow.user == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        Follow = apps.get_model('followers', 'Follow')
        if Follow.objects.filter(follower=request.user.profile, followed=profile_to_follow).exists():
            return Response({'error': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(follower=request.user.profile, followed=profile_to_follow)
        return Response({'status': 'followed'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        profile_to_unfollow = self.get_object()
        Follow = apps.get_model('followers', 'Follow')
        follow_instance = Follow.objects.filter(follower=request.user.profile, followed=profile_to_unfollow)
        if follow_instance.exists():
            follow_instance.delete()
            return Response({'status': 'unfollowed'})
        else:
            return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Profile.objects.select_related('user').prefetch_related('user__followers', 'user__following')
        if self.action not in ['list', 'retrieve']:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

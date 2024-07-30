from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer


# Create your views here.

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.profile  
        return Notification.objects.filter(recipient=user_profile).order_by('-created_at')

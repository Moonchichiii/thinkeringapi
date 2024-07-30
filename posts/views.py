
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from backend.pagination import StandardResultsSetPagination
from .serializers import PostSerializer
from backend.permissions import IsOwnerOrReadOnly
from profiles.models import Profile

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=profile)

    @action(detail=False, methods=['get'], filter_backends=(DjangoFilterBackend,))
    def search(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    @transaction.atomic
    def approve(self, request, pk=None):
        try:
            post = self.get_object()
            post.approved = True
            post.save()
            return Response({'status': 'post approved'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An error occurred during approval."}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        posts = self.get_queryset().filter(average_rating__gte=4).order_by('-average_rating', '-rating_count')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def category(self, request, *args, **kwargs):
        category_name = request.query_params.get('name', None)
        if category_name:
            posts = self.get_queryset().filter(tags__name=category_name, tags__is_category=True)
            page = self.paginate_queryset(posts)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({"error": "Category name not provided."}, status=status.HTTP_400_BAD_REQUEST)

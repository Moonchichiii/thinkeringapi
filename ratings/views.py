from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Rating
from .serializers import RatingSerializer


# Create your views here.

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all().select_related('profile', 'post')
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = serializer.validated_data['post']
        rating = serializer.validated_data['rating']

        if not 1 <= rating <= 5:
            return Response({"error": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                existing_rating = Rating.objects.filter(profile=request.user.profile, post=post).first()

                if existing_rating:
                    old_rating = existing_rating.rating
                    existing_rating.rating = rating
                    existing_rating.save()
                    post.average_rating = (post.average_rating * post.rating_count - old_rating + rating) / post.rating_count
                else:
                    serializer.save(profile=request.user.profile)
                    post.rating_count += 1
                    post.average_rating = (post.average_rating * (post.rating_count - 1) + rating) / post.rating_count
                post.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "An error occurred while saving the rating."}, status=status.HTTP_400_BAD_REQUEST)

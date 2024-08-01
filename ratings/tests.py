from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction, IntegrityError
from rest_framework import status
from profiles.models import Profile
from posts.models import Post
from ratings.models import Rating


# Create your tests here.

class RatingTests(APITestCase):
    def setUp(self):
        try:
            self.user = User.objects.create_user(username='testuser', password='password')
            self.profile = Profile.objects.get(user=self.user)
            self.post = Post.objects.create(author=self.profile, title='Test Post', content='Test Content')
            refresh = RefreshToken.for_user(self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        except IntegrityError:
            transaction.rollback()

    def tearDown(self):
        Rating.objects.all().delete()
        Post.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_create_rating(self):
        data = {'post': self.post.id, 'rating': 5}
        response = self.client.post('/api/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_ratings(self):
        Rating.objects.create(profile=self.profile, post=self.post, rating=5)
        response = self.client.get('/api/ratings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_rating(self):
        rating = Rating.objects.create(profile=self.profile, post=self.post, rating=3)
        data = {'rating': 4}
        response = self.client.patch(f'/api/ratings/{rating.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 4)

    def test_prevent_duplicate_ratings(self):
        Rating.objects.create(profile=self.profile, post=self.post, rating=3)
        data = {'post': self.post.id, 'rating': 5}
        response = self.client.post('/api/ratings/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_ratings_for_post(self):
        Rating.objects.create(profile=self.profile, post=self.post, rating=5)
        response = self.client.get(f'/api/ratings/?post={self.post.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

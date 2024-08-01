from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from profiles.models import Profile
from posts.models import Post
from likes.models import Like

# Create your tests here.
class LikeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.get(user=self.user)
        self.post = Post.objects.create(author=self.profile, title='Test Post', content='Test Content')
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_like(self):
        response = self.client.post('/api/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_delete_like(self):
        like = Like.objects.create(profile=self.profile, post=self.post)
        response = self.client.delete(f'/api/likes/{like.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_prevent_duplicate_likes(self):
        Like.objects.create(profile=self.profile, post=self.post)
        response = self.client.post('/api/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
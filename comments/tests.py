from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from profiles.models import Profile
from posts.models import Post
from comments.models import Comment


# Create your tests here.


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.get(user=self.user)
        self.post = Post.objects.create(author=self.profile, title='Test Post', content='Test Content')
        self.comment = Comment.objects.create(post=self.post, author=self.profile, content='Test Comment')
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def tearDown(self):
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_create_comment(self):
        data = {'post': self.post.id, 'content': 'Test Comment'}
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)  # Original comment and new comment

    def test_update_comment(self):
        data = {'content': 'Updated Comment'}
        response = self.client.put(f'/api/comments/{self.comment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated Comment')

    def test_delete_comment(self):
        comment_id = self.comment.id
        response = self.client.delete(f'/api/comments/{comment_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

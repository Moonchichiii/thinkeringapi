from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile
from posts.models import Post
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.


class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.get(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post_data = {'title': 'Test Post', 'content': 'Test Content'}

    def test_create_post(self):
        response = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_get_posts(self):
        Post.objects.create(author=self.profile, title='Test Post', content='Test Content')
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_delete_post(self):
        post = Post.objects.create(author=self.profile, title='Test Post', content='Test Content')
        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_update_post(self):
        post = Post.objects.create(author=self.profile, title='Test Post', content='Test Content')
        update_data = {'title': 'Updated title', 'content': 'Updated content'}
        response = self.client.patch(f'/api/posts/{post.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated title')
        self.assertEqual(post.content, 'Updated content')

    def test_search_posts(self):
        Post.objects.create(author=self.profile, title='Searchable Post', content='Searchable content')
        response = self.client.get('/api/posts/', {'search': 'Searchable'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

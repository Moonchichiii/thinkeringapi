from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from profiles.models import Profile
from chatbot.views import ChatbotView
from django.contrib.auth.models import User
from ratings.models import Rating
from posts.models import Post


# Create your tests here.

class ChatbotTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.get(user=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def tearDown(self):        
        Rating.objects.all().delete()
        Post.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        self.client.logout()

    def test_update_profile_via_chatbot(self):
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'update profile bio: New bio'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Profile updated successfully', response.data['response'])

    def test_no_message_provided_to_chatbot(self):
        response = self.client.post(reverse('chatbot:chatbot'), {'message': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No message provided', response.data['error'])

    def test_invalid_message_to_chatbot(self):
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'invalid command'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('Search Results', response.data['response'])
        self.assertNotIn('Profile updated successfully', response.data['response'])
        self.assertNotIn('Post created', response.data['response'])

    def test_unauthorized_create_post_via_chatbot(self):
        self.client.logout()
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'create post title: Test, content: This is a test post'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_profile_via_chatbot(self):
        self.client.logout()
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'update profile bio: New bio, avatar: new_avatar.jpg'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_posts_via_chatbot(self):
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'search posts Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Search Results', response.data['response'])

    def test_search_posts_with_empty_query_via_chatbot(self):
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'search posts '}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No search query provided', response.data['response'])

    def test_malformed_update_profile_command(self):
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'update profile bio:'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No valid profile data provided.', response.data['response'])

    def test_create_post_with_missing_data_via_chatbot(self):
        response = self.client.post(reverse('chatbot:chatbot'), {'message': 'create post title: , content: '}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Missing title or content for the post.', response.data['response'])

    def test_extract_profile_data(self):
        chatbot_view = ChatbotView()
        message = "update profile bio: New bio"
        data = chatbot_view.extract_profile_data(message)
        self.assertEqual(data['bio'], 'New bio')

    def test_extract_post_data(self):
        chatbot_view = ChatbotView()
        message = "create post title: Test Title, content: Test content"
        data = chatbot_view.extract_post_data(message)
        self.assertEqual(data['title'], 'Test Title')
        self.assertEqual(data['content'], 'Test content')

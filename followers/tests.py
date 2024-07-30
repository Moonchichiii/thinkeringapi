from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from .models import Follow


# Create your tests here.

class FollowTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user1 = User.objects.create_user(username='user1', password='pass1234')
        cls.user2 = User.objects.create_user(username='user2', password='pass1234')
        cls.user3 = User.objects.create_user(username='user3', password='pass1234')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    @classmethod
    def tearDownClass(cls):
        cls.client.force_authenticate(user=None)
        User.objects.all().delete()
        Follow.objects.all().delete()

    def test_create_follow(self):
        response = self.client.post(reverse('followers:follow-list-create'), {'followed': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(Follow.objects.first().follower, self.user1)
        self.assertEqual(Follow.objects.first().followed, self.user2)

    def test_create_follow_missing_id(self):
        response = self.client.post(reverse('followers:follow-list-create'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'This field is required.')

    def test_create_follow_nonexistent_user(self):
        response = self.client.post(reverse('followers:follow-list-create'), {'followed': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User not found.')

    def test_prevent_duplicate_follow(self):
        Follow.objects.create(follower=self.user1, followed=self.user2)
        response = self.client.post(reverse('followers:follow-list-create'), {'followed': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'You are already following this user.')

    def test_unfollow(self):
        follow = Follow.objects.create(follower=self.user1, followed=self.user2)
        response = self.client.delete(reverse('followers:follow-destroy', kwargs={'pk': self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 0)

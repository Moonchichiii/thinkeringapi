from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from profiles.models import Profile
from followers.models import Follow

# Create your tests here.

class FollowTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user1 = User.objects.create_user(username='user1', password='pass1234')
        cls.user2 = User.objects.create_user(username='user2', password='pass1234')
        cls.user3 = User.objects.create_user(username='user3', password='pass1234')

        cls.profile1 = Profile.objects.get(user=cls.user1)
        cls.profile2 = Profile.objects.get(user=cls.user2)
        cls.profile3 = Profile.objects.get(user=cls.user3)

    def setUp(self):
        self.client.force_authenticate(user=self.user1)

    def tearDown(self):
        Follow.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        cls.client.force_authenticate(user=None)
        User.objects.all().delete()

    def test_create_follow(self):
        response = self.client.post(reverse('followers:follow-list-create'), {'followed': self.profile2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(Follow.objects.first().follower, self.profile1)
        self.assertEqual(Follow.objects.first().followed, self.profile2)

    def test_create_follow_missing_id(self):
        response = self.client.post(reverse('followers:follow-list-create'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_follow_nonexistent_user(self):
        response = self.client.post(reverse('followers:follow-list-create'), {'followed': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_prevent_duplicate_follow(self):
        Follow.objects.create(follower=self.profile1, followed=self.profile2)
        response = self.client.post(reverse('followers:follow-list-create'), {'followed': self.profile2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow(self):
        follow = Follow.objects.create(follower=self.profile1, followed=self.profile2)
        response = self.client.delete(reverse('followers:follow-destroy', kwargs={'pk': follow.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 0)

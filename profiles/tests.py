from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from profiles.models import Profile
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile
from django.test import TransactionTestCase



# Create your tests here.

class ProfileTests(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_update_profile(self):
        profile = Profile.objects.get(user=self.user)
        response = self.client.put(f'/api/profiles/{profile.id}/', {'bio': 'New bio'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'New bio')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_profile_str(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), self.user.username)
    
    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_model', password='password')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsInstance(profile, Profile)

    def test_profile_str(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), self.user.username)
        
    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

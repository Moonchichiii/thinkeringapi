from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from profiles.models import Profile
from tags.models import Tag


# Create your tests here.

class TagInitialDataTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_initial_tag_data(self):
        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 0, "There should be no initial tags.")
    
    def test_list_tags(self):
        Tag.objects.create(name='testtag1', profile=self.profile)
        Tag.objects.create(name='testtag2', profile=self.profile)
        
        response = self.client.get(reverse('tags:tag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

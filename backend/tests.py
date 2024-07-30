from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from profiles.models import Profile
from posts.views import PostViewSet
from backend.views import HomeViewSet
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.test import RequestFactory


class UrlsTestCase(TestCase):
    def test_home_url_resolves(self):
        # Test if the home URL resolves to HomeViewSet
        url = reverse('home-list')
        self.assertEqual(resolve(url).func.cls, HomeViewSet)

    def test_admin_url_resolves(self):
        # Test if the admin URL resolves
        url = reverse('admin:index')
        self.assertTrue(resolve(url).func)

    def test_auth_urls_resolve(self):
        # Test if authentication URLs resolve correctly
        url = reverse('rest_login')
        self.assertTrue(resolve(url).func)

    def test_api_urls_resolve(self):
        # Test if the post list API URL resolves
        url = reverse('posts:post-list')
        self.assertEqual(resolve(url).func.cls, PostViewSet)

class IsOwnerOrReadOnlyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='password1')
        self.user2 = User.objects.create_user(username='testuser2', password='password2')
        self.client.force_authenticate(user=self.user1)
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        Profile.objects.all().delete()

    def test_non_owner_has_no_permission(self):
        # Test if a non-owner cannot access another's profile
        response = self.client.get(f'/api/profiles/{self.profile2.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_has_permission(self):
        # Test if the owner can access their own profile
        response = self.client.get(f'/api/profiles/{self.profile1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ASGITestCase(TestCase):
    def test_asgi_application(self):
        # Test if the ASGI application is correctly set up
        application = get_asgi_application()
        self.assertIsNotNone(application)

class WSGITestCase(TestCase):
    def test_wsgi_application(self):
        # Test if the WSGI application is correctly set up
        application = get_wsgi_application()
        self.assertIsNotNone(application)

class SettingsTestCase(TestCase):
    def test_installed_apps(self):
        # Test if 'rest_framework' is in installed apps
        self.assertIn('rest_framework', settings.INSTALLED_APPS)

    def test_jwt_settings(self):
        # Test if JWT settings are correctly configured
        self.assertIn('rest_framework_simplejwt.authentication.JWTAuthentication',
                      settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'])

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_session_middleware(self):
        # Test if session middleware processes requests correctly
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda req: HttpResponse("OK"))
        middleware.process_request(request)
        request.session.save()
        response = middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_authentication_middleware(self):
        # Test if authentication middleware processes requests correctly
        request = self.factory.get('/')
        session_middleware = SessionMiddleware(lambda req: None)
        session_middleware.process_request(request)
        request.session.save()
        middleware = AuthenticationMiddleware(lambda req: HttpResponse("OK"))
        response = middleware(request)
        self.assertEqual(response.status_code, 200)

class HomeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='password1')
        self.user2 = User.objects.create_user(username='testuser2', password='password2')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

    def test_home_list(self):
        # Test home list view
        response = self.client.get(reverse('home-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the Home Page")

    def test_non_owner_has_no_permission(self):
        # Test non-owner access restriction
        response = self.client.get(f'/api/profiles/{self.profile2.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from profiles.models import Profile
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase
from users.serializers import RegisterSerializer, UserSerializer

class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.get(user=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.client.login(username='testuser', password='password')

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_get_current_user(self):
        response = self.client.get(reverse('users:current_user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'uniqueuser',
            'email': 'uniqueuser@example.com',
            'password1': 'StrongPassword@123',
            'password2': 'StrongPassword@123'
        }
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = Profile.objects.get(user=self.user)

    def test_register_serializer(self):
        serializer = RegisterSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")
        user = serializer.save()
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['profile']['bio'], self.profile.bio)


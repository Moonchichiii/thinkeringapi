from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from profiles.models import Profile
from posts.views import PostViewSet
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from rest_framework_simplejwt.tokens import RefreshToken
from backend.serializers import RegisterSerializer, UserSerializer



class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = [SessionMiddleware, AuthenticationMiddleware]

    def test_session_middleware(self):
        request = self.factory.get('/')
        for mw in self.middleware:
            mw(lambda req: HttpResponse("OK")).process_request(request)
        request.session.save()
        response = HttpResponse("OK")
        self.assertEqual(response.status_code, 200)


class UrlsTestCase(TestCase):
    def test_admin_url_resolves(self):
        url = reverse('admin:index')
        self.assertTrue(resolve(url).func)

    def test_auth_urls_resolve(self):
        url = reverse('rest_login')
        self.assertTrue(resolve(url).func)

    def test_api_urls_resolve(self):
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
        response = self.client.get(f'/api/profiles/{self.profile2.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_has_permission(self):
        response = self.client.get(f'/api/profiles/{self.profile1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ASGITestCase(TestCase):
    def test_asgi_application(self):
        application = get_asgi_application()
        self.assertIsNotNone(application)


class WSGITestCase(TestCase):
    def test_wsgi_application(self):
        application = get_wsgi_application()
        self.assertIsNotNull(application)


class SettingsTestCase(TestCase):
    def test_installed_apps(self):
        self.assertIn('rest_framework', settings.INSTALLED_APPS)

    def test_jwt_settings(self):
        self.assertIn('rest_framework_simplejwt.authentication.JWTAuthentication',
                      settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'])


class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_session_middleware(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda req: HttpResponse("OK"))
        middleware.process_request(request)
        request.session.save()
        response = middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_authentication_middleware(self):
        request = self.factory.get('/')
        session_middleware = SessionMiddleware(lambda req: None)
        session_middleware.process_request(request)
        request.session.save()
        middleware = AuthenticationMiddleware(lambda req: HttpResponse("OK"))
        response = middleware(request)
        self.assertEqual(response.status_code, 200)


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
        response = self.client.get(reverse('current_user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        response = self.client.post(reverse('logout'))
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

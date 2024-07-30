from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from profiles.serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

    
    
    

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'detail': 'User registered successfully.'
            }
            response = Response(response_data, status=status.HTTP_201_CREATED)
            secure_cookie = request.is_secure()
            response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=secure_cookie, samesite='None')
            response.set_cookie('refresh_token', str(refresh), httponly=True, secure=secure_cookie, samesite='None')
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            tokens = response.data
            secure_cookie = request.is_secure()
            response.set_cookie('access_token', tokens['access'], httponly=True, secure=secure_cookie, samesite='None')
            response.set_cookie('refresh_token', tokens['refresh'], httponly=True, secure=secure_cookie, samesite='None')
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            tokens = response.data
            secure_cookie = request.is_secure()
            response.set_cookie('access_token', tokens['access'], httponly=True, secure=secure_cookie, samesite='None')
        return response

class UpdateEmailView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        user_data = self.get_serializer(user).data
        return Response(user_data)
    
    # CSRF token view
    def get_csrf_token(request):
        return JsonResponse({'csrfToken': get_token(request)})

    
    
    

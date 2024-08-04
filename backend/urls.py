from django.contrib import admin
from django.urls import path, include
from .views import (
    RegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, 
    LogoutView, CurrentUserView, UpdateEmailView, GetCsrftoken
)
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/auth/social/', include('allauth.urls')),
    path('api/v1/get-csrf-token/', GetCsrftoken.as_view(), name='get_csrf_token'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/v1/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/current_user/', CurrentUserView.as_view(), name='current_user'),
    path('api/v1/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/update_email/', UpdateEmailView.as_view(), name='update_email'),
    path('api/v1/posts/', include('posts.urls', namespace='posts')),
    path('api/v1/comments/', include('comments.urls', namespace='comments')),
    path('api/v1/likes/', include('likes.urls', namespace='likes')),
    path('api/v1/ratings/', include('ratings.urls', namespace='ratings')),
    path('api/v1/followers/', include('followers.urls', namespace='followers')),
    path('api/v1/profiles/', include('profiles.urls', namespace='profiles')),
    path('api/v1/notifications/', include('notifications.urls', namespace='notifications')),
    path('api/v1/chatbot/', include('chatbot.urls', namespace='chatbot')),
    path('api/v1/tags/', include('tags.urls', namespace='tags')),
]

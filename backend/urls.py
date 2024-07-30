from django.contrib import admin
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView, CurrentUserView, UpdateEmailView, get_csrf_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.urls')),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),    
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('current_user/', CurrentUserView.as_view(), name='current_user'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    
    
    path('api/posts/', include('posts.urls', namespace='posts')),
    path('api/comments/', include('comments.urls', namespace='comments')),
    path('api/likes/', include('likes.urls', namespace='likes')),
    path('api/ratings/', include('ratings.urls', namespace='ratings')),
    path('api/followers/', include('followers.urls', namespace='followers')),
    path('api/profiles/', include('profiles.urls', namespace='profiles')),
    path('api/notifications/', include('notifications.urls', namespace='notifications')),
    path('api/chatbot/', include('chatbot.urls', namespace='chatbot')),
    path('api/tags/', include('tags.urls', namespace='tags')),
]



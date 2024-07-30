from django.urls import path
from .views import FollowListCreateView, FollowDestroyView

app_name = 'followers'

urlpatterns = [
    path('', FollowListCreateView.as_view(), name='follow-list-create'),
    path('<int:pk>/unfollow/', FollowDestroyView.as_view(), name='follow-destroy'),
]

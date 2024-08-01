from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile
from posts.models import Post
from comments.models import Comment
from likes.models import Like
from followers.models import Follow
from notifications.models import Notification
from notifications import handlers, signals
from django.core.cache import cache


# Create your tests here.





class NotificationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)
        self.post = Post.objects.create(author=self.profile1, title='Test Post', content='Content')

        # Connect signals for testing
        signals.create_notification_for_comment.connect(handlers.create_notification_for_comment_handler)
        signals.create_notification_for_follow.connect(handlers.create_notification_for_follow_handler)
        signals.create_notification_for_like.connect(handlers.create_notification_for_like_handler)

    def tearDown(self):
        signals.create_notification_for_comment.disconnect(handlers.create_notification_for_comment_handler)
        signals.create_notification_for_follow.disconnect(handlers.create_notification_for_follow_handler)
        signals.create_notification_for_like.disconnect(handlers.create_notification_for_like_handler)

    @patch('notifications.handlers.create_notification_for_comment_handler')
    def test_create_comment_notification(self, mock_handler):
        Comment.objects.create(post=self.post, author=self.profile2, content='Test Comment')
        mock_handler.assert_called_once()

    @patch('notifications.handlers.create_notification_for_follow_handler')
    def test_create_follow_notification(self, mock_handler):
        Follow.objects.create(follower=self.profile1, followed=self.profile2)
        mock_handler.assert_called_once()

    @patch('notifications.handlers.create_notification_for_like_handler')
    def test_create_like_notification(self, mock_handler):
        Like.objects.create(post=self.post, profile=self.profile2)
        mock_handler.assert_called_once()

    def test_notification_creation(self):
        Comment.objects.create(post=self.post, author=self.profile2, content='Test Comment')
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.profile1)
        self.assertEqual(notification.actor, self.profile2)
        self.assertEqual(notification.verb, 'commented on')

    def test_notification_str_representation(self):
        Comment.objects.create(post=self.post, author=self.profile2, content='Test Comment')
        notification = Notification.objects.first()
        expected_str = f'Notification: {notification.actor} commented on {notification.target} {notification.created_at}'
        self.assertEqual(str(notification), expected_str)

    def create_notification_for_like_handler(sender, instance, **kwargs):
        rate_limit_key = f'notification_rate_limit:{instance.profile.id}'
        if not cache.get(rate_limit_key):
            cache.set(rate_limit_key, 0)
            cache.incr(rate_limit_key)

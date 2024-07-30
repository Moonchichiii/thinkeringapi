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

# Create your tests here.
class NotificationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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
        # Disconnect signals after each test
        signals.create_notification_for_comment.disconnect(handlers.create_notification_for_comment_handler)
        signals.create_notification_for_follow.disconnect(handlers.create_notification_for_follow_handler)
        signals.create_notification_for_like.disconnect(handlers.create_notification_for_like_handler)

    @patch('notifications.handlers.create_notification_for_comment_handler')
    def test_create_comment_notification(self, mock_handler):
        comment = Comment.objects.create(post=self.post, author=self.profile2, content='Test Comment')
        mock_handler.assert_called_once()
        args, kwargs = mock_handler.call_args
        self.assertEqual(kwargs['sender'], Comment)
        self.assertIsInstance(kwargs['instance'], Comment)
        self.assertIn('signal', kwargs)

    @patch('notifications.handlers.create_notification_for_follow_handler')
    def test_create_follow_notification(self, mock_handler):
        follow = Follow.objects.create(follower=self.user1, followed=self.user2)
        mock_handler.assert_called_once()
        args, kwargs = mock_handler.call_args
        self.assertEqual(kwargs['sender'], Follow)
        self.assertIsInstance(kwargs['instance'], Follow)
        self.assertIn('signal', kwargs)

    @patch('notifications.handlers.create_notification_for_like_handler')
    def test_create_like_notification(self, mock_handler):
        like = Like.objects.create(post=self.post, profile=self.profile2)
        mock_handler.assert_called_once()
        args, kwargs = mock_handler.call_args
        self.assertEqual(kwargs['sender'], Like)
        self.assertIsInstance(kwargs['instance'], Like)
        self.assertIn('signal', kwargs)

    def test_notification_creation(self):
        Comment.objects.create(post=self.post, author=self.profile2, content='Test Comment')
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.actor, self.user2)
        self.assertEqual(notification.verb, 'commented on')

    def test_notification_str_representation(self):
        Comment.objects.create(post=self.post, author=self.profile2, content='Test Comment')
        notification = Notification.objects.first()
        expected_str = f'Notification: {self.user2} commented on {self.post} {notification.created_at}'
        self.assertEqual(str(notification), expected_str)




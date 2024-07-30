from django.db import models
from profiles.models import Profile
from posts.models import Post
from notifications.signals import create_notification_for_comment

class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.content[:20]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            create_notification_for_comment.send(sender=self.__class__, instance=self)

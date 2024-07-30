from django.db import models
from profiles.models import Profile
from posts.models import Post
from notifications.signals import create_notification_for_like

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile} likes {self.post}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            create_notification_for_like.send(sender=self.__class__, instance=self)

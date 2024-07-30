from django.db import models
from profiles.models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from notifications.signals import create_notification_for_follow
from profiles.models import Profile


# Create your models here.

class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.followed.user.username}"

    def clean(self):
        if self.follower == self.followed:
            raise ValidationError(_("You cannot follow yourself."))

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            create_notification_for_follow.send(sender=self.__class__, instance=self)

    @property
    def follow_duration(self):
        return timezone.now() - self.created_at

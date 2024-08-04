from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
from profiles.models import Profile
from tags.models import Tag
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = CloudinaryField('image', blank=True, null=True, transformation={"format": "webp"})
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    average_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        from likes.models import Like
        return Like.objects.filter(post=self).count()
   
    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        if self.image and (self.image.size > 2 * 1024 * 1024 or not self.image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))):
            raise ValidationError("Invalid image file: must be less than 2MB and in PNG, JPG, JPEG, or WEBP format.")

@receiver(m2m_changed, sender=Post.tags.through)
def notify_tagged_profiles(sender, instance, action, **kwargs):
    if action == "post_add":
        tagged_profiles = instance.tags.all()
        for tag in tagged_profiles:
            Notification.objects.create(
                profile=tag.profile,
                content=f"You have been tagged in a post titled '{instance.title}'",
                content_type=ContentType.objects.get_for_model(Post),
                object_id=instance.id
            )

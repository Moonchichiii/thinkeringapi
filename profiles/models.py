from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from cloudinary import api
from cloudinary.exceptions import Error as CloudinaryError
from django.core.exceptions import ValidationError
from django.apps import apps

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = CloudinaryField('avatar', blank=True, null=True, transformation={"format": "webp"})

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.avatar:
            try:
                resource_info = api.resource(self.avatar.public_id)
                if resource_info['bytes'] > 2 * 1024 * 1024:
                    raise ValidationError("Avatar file size must be less than 2MB.")
            except CloudinaryError as e:
                raise ValidationError(f"Error retrieving image info: {str(e)}")
            except AttributeError:
                if self.avatar.size > 2 * 1024 * 1024:
                    raise ValidationError("Avatar file size must be less than 2MB.")

    def followers_count(self):
        Follow = apps.get_model('followers', 'Follow')
        return Follow.objects.filter(followed=self).count()

    def following_count(self):
        Follow = apps.get_model('followers', 'Follow')
        return Follow.objects.filter(follower=self).count() 

    class Meta:
        ordering = ['user__username']
        
    @property
    def post_count(self):
        return self.posts.count()  # 'posts' comes from the related_name in Post model's 'author' field

    @property
    def is_popular(self):
        # Define your popularity logic here, e.g., based on the number of posts
        return self.post_count > 10


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

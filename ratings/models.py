from django.db import models
from profiles.models import Profile
from posts.models import Post

# Create your models here.


class Rating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('profile', 'post')
        ordering = ['-rating']

    def __str__(self):
        return f'{self.profile} rated {self.post} with {self.rating}'

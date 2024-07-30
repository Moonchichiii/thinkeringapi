from django.db import models
from profiles.models import Profile


# Create your models here.

TAG_TYPE_CHOICES = (
    ('regular', 'Regular'),
    ('category', 'Category'),
)

class Tag(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tag_type = models.CharField(max_length=10, choices=TAG_TYPE_CHOICES, default='regular')
     
   
    def __str__(self):
        return self.name

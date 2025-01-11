from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweets(models.Model):
    tweet = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return (f"{self.user.username} ({self.created_at}): {self.tweet}")
    class Meta:
        verbose_name_plural = 'Tweets'
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    last_change = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.jpg')
    bio = models.TextField(null=True, blank=True, max_length=240)
   
    website = models.URLField(null=True, blank=True, default="", max_length=100)
    instagram = models.URLField(null=True, blank=True, default="", max_length=100)
    facebook = models.URLField(null=True, blank=True, default="", max_length=100)
    x = models.URLField(null=True, blank=True, default="", max_length=100) 
  
    def __str__(self):
        return self.user.username
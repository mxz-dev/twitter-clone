from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweets(models.Model):
    tweet = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return (f"{self.user.username} ({self.created_at}): {self.tweet}")
    class Meta:
        verbose_name_plural = 'Tweets'
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    last_change = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.jpg')
    def __str__(self):
        return self.user.username
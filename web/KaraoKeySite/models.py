from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
  first_name  = models.CharField(max_length=20)
  last_name   = models.CharField(max_length=20)

class Song(models.Model):

    audio_file = models.FileField(upload_to='songs/', null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    # lyrics ?
    # notes ?
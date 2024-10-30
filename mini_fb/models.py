# blog/models.py
# Define data models (objects) for use in the blog application
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.first} {self.last}"

    def get_status_messages(self):
        return self.statusmessage_set.order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})


class StatusMessage(models.Model):

    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Status by {self.profile.first} {self.profile.last} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

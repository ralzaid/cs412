from django.db import models
from django.utils import timezone
from django.urls import reverse


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
    
    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        friends = [friend.profile2 for friend in friends_as_profile1] + [friend.profile1 for friend in friends_as_profile2]

        return friends
    def add_friend(self, other):
        if self != other:
            if not Friend.objects.filter(
                models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
            ).exists():
                Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        friends = self.get_friends()
        friend_ids = [friend.id for friend in friends]
        friend_ids.append(self.id)
        return Profile.objects.exclude(id__in=friend_ids)
    
    def get_news_feed(self):
        own_statuses = StatusMessage.objects.filter(profile=self)

        friend_profiles = self.get_friends()
        friend_statuses = StatusMessage.objects.filter(profile__in=friend_profiles)

        news_feed = own_statuses | friend_statuses
        return news_feed.order_by('-timestamp')



class StatusMessage(models.Model):

    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Status by {self.profile.first} {self.profile.last} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_images(self):
        return self.image_set.all()


class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for StatusMessage {self.status_message.id} at {self.timestamp}"
    

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"

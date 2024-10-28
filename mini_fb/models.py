# blog/models.py
# Define data models (objects) for use in the blog application
from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data for a blog Article by some author.'''

    # data attributes:
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Article.'''
        return f"{self.first} {self.last}"
     
    
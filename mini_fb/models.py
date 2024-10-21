# Author: Keith Yeung 
# Email: keithy@bu.edu 
# this is a model for Profiles
## mini_fb/models.py
from django.db import models
from django.urls import reverse ## NEW


# Create your models here.

class Profile(models.Model):
  '''This will model the data attributes of Facebook Users'''

  #data attributes of Profile
  Fname = models.TextField(blank=False)
  Lname = models.TextField(blank=False)
  city = models.TextField(blank=False)
  email = models.TextField(blank=False)
  address = models.TextField(blank=False)
  profile_url = models.URLField(blank=True)

  def __str__(self):
    '''Return a string representation of this object.'''

    return f'{self.Fname} {self.Lname}'
  
  def get_status_message(self):
    '''Return all of the status message about this profile'''
    message = StatusMessage.objects.filter(profile=self)
    return message
  
  def get_absolute_url(self):
    '''returns the URL for the object’s detailed view'''
    return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
  '''This will model the data attributes of Status Message'''

  timestamp = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=False)
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

  def __str__(self):
        '''Return a string representation of this Status Message object.'''
        return f'{self.message}'
  
  def get_images(self):
    '''Return all of the images about this status message'''
    images = Image.objects.filter(status_message=self)
    return images

class Image(models.Model):
    image_file = models.ImageField(blank=True)  
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.status_message.message} uploaded at {self.uploaded_at}"

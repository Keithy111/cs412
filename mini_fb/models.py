# Author: Keith Yeung 
# Email: keithy@bu.edu 
# this is a model for Profiles
## mini_fb/models.py
from django.db import models

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

class StatusMessage(models.Model):
  '''This will model the data attributes of Status Message'''

  timestamp = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=False)
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

  def __str__(self):
        '''Return a string representation of this Status Message object.'''
        return f'{self.message}'
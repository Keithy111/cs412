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
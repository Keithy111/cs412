# Author: Keith Yeung 
# Email: keithy@bu.edu 
# this is a model for Profiles
## mini_fb/models.py
from django.db import models
from django.urls import reverse ## NEW
from django.utils import timezone


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
  
  def get_friends(self):
    """Return all friends related to a profile."""
    all_friends = []
    # Loop through Friend relationships and add each linked friend to the list
    friendships1 = Friend.objects.filter(profile1=self)
    friendships2 = Friend.objects.filter(profile2=self)
    
    for friendship in friendships1:
        all_friends.append(friendship.profile2)  # profile2 is the friend of profile1 (self)
    
    for friendship in friendships2:
        all_friends.append(friendship.profile1)  # profile1 is the friend of profile2 (self)
        
    return all_friends
  
  def add_friend(self, friend):
       """Add a Friend relation between self and another friend."""
       if self != friend and friend not in self.get_friends():  
        Friend.objects.create(profile1=self, profile2=friend)
  
  def get_friend_suggestions(self):
    """Return a list of possible friends for this Profile."""
    # Get all profiles excluding the current profile
    all_profiles = list(Profile.objects.all())
    
    # Get all friends of the current profile
    friends = Friend.objects.filter(
        models.Q(profile1=self) | models.Q(profile2=self)
    )
    friend_ids = set()
    for friendship in friends:
        friend_ids.add(friendship.profile1.id if friendship.profile1 != self else friendship.profile2.id)

    suggestions = [
        profile for profile in all_profiles 
        if profile.id != self.id and profile.id not in friend_ids
    ]
    return suggestions
  
  def get_news_feed(self):
     ''' Return a StatusMessages of the user and friends '''

     user_status = StatusMessage.objects.filter(profile=self)
     friends = self.get_friends()
     friend_status = StatusMessage.objects.filter(profile__in=friends)
     news_feed = user_status.union(friend_status).order_by('-timestamp')
     return news_feed
  
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
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Image {self.id} for StatusMessage {self.status_message.id}"


class Friend(models.Model):
    """This model represents a friendship between two Profiles."""

    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Friend relationship."""
        return f"{self.profile1.Fname} {self.profile1.Lname} & {self.profile2.Fname} {self.profile2.Lname} " 

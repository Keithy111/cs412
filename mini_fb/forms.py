# Author: Keith Yeung 
# Email: keithy@bu.edu 
# this is a form for mini_fb
## mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
  '''A form to add a Profile to the database'''

  class Meta:
    model = Profile
    fields = ['Fname', 'Lname', 'city', 'email', 'address', 'profile_url'] # which fields to include in the form]

class CreateStatusMessageForm(forms.ModelForm):
  '''A form to create status messsage to the database'''
  class Meta:
    model = StatusMessage
    fields = ['message'] # which fields to include in the form]
  
class UpdateProfileForm(forms.ModelForm):
    '''Form to update the user's profile. Excludes first name and last name.'''

    class Meta:
        model = Profile
        fields = ['Fname', 'Lname', 'city', 'email', 'address', 'profile_url']
        # Explicitly listing the fields to include, excluding first name (Fname) and last name (Lname)

class StatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']  # Only allow updating the 'message' field
        
        

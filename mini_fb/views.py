# Author: Keith Yeung 
# Email: keithy@bu.edu 
# This a Django class-based view (ShowAllProfiles) that uses ListView to display all Profile objects from the database in a template named 'mini_fb/show_all_profiles.html'.
# #mini_fb/views.py

from .models import Profile # import the models(Profile)
from django.views.generic import ListView

# Create your views here.
class ShowAllProfiles(ListView):
    '''Create a subclass of ListView to display all blog articles.'''

    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

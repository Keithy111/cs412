# Author: Keith Yeung 
# Email: keithy@bu.edu 
# This a Django class-based view (ShowAllProfiles) that uses ListView to display all Profile objects from the database in a template named 'mini_fb/show_all_profiles.html'.
# #mini_fb/views.py

from .models import Profile, StatusMessage, Image 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import *
from django.urls import reverse ## NEW
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect ## NEW


# Create your views here.
class ShowAllProfiles(ListView):
    '''Create a subclass of ListView to display all blog articles.'''

    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Display one Article selected at Random'''

    model = Profile # the model to display
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    ''' a view to create a profile'''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_absolute_url(self):
        '''returns the URL for the object’s detailed view'''
        return reverse('show_profile', kwargs={'pk': self.pk})
        
class CreateStatusMessageView(CreateView):
    '''A view to show/process the create status message form'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successful create'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('show_profile', kwargs={'pk': profile.pk})

    def form_valid(self, form):
        '''This method executes after form submission'''

        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile

        # Save the form to store the new StatusMessage in the database
        sm = form.save()

        # Handle file uploads (the name 'files' should match the input name in the form)
        files = self.request.FILES.getlist('files')
        for f in files:
            # Create a new Image object for each file without the 'timestamp' field
            image = Image(
                image_file=f,  # Set the file in the ImageField
                status_message=sm  # Link the image to the status message
            )
            image.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        '''Build the template context data -- a dict of key-value pairs.'''

        # Get the super class version of context data
        context = super().get_context_data(**kwargs)

        # Find the profile with the PK from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # Add the profile to the context data
        context['profile'] = profile

        return context


class UpdateProfileView(UpdateView):
    '''Class-based view for updating a user's profile.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Override to redirect to the updated profile's detail page.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        '''Add additional context data to the template.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object  # Add the profile instance to the context
        return context

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect back to the profile page after successful delete
        profile_pk = self.object.profile.pk  # Get the profile pk from the status message
        return reverse('show_profile', kwargs={'pk': profile_pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = StatusMessageForm  # Form to update the status message text
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'st_msg'
    
    def get_success_url(self):
        # Redirect the user back to the profile page after successful update
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(View):
    ''' A view that allows a user to add a friend '''
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            return self.post(request, *args, **kwargs)
        return self.http_method_not_allowed(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        profile_pk = kwargs.get('pk')
        other_pk = kwargs.get('other_pk')
        profile = Profile.objects.get(pk=profile_pk)
        other_profile = Profile.objects.get(pk=other_pk)

        profile.add_friend(other_profile)
        return HttpResponseRedirect(self.get_success_url(profile.pk))
    
    def get_success_url(self, pk):
        ''' Return the URL to redirect to after adding a friend '''
        return reverse('show_profile', kwargs={'pk': pk})

class ShowFriendSuggestionsView(DetailView):
    ''' A view to see friend suggestions '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
    def get_success_url(self):
        ''' Return the URL to redirect to after successful update '''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class ShowNewsFeedView(DetailView):
    ''' A view to see other status messages of friends '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        context['current_profile'] = profile
        return context

    

# Author: Keith Yeung 
# Email: keithy@bu.edu 
# This a Django class-based view (ShowAllProfiles) that uses ListView to display all Profile objects from the database in a template named 'mini_fb/show_all_profiles.html'.
# #mini_fb/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, StatusMessage, Image, Friend
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, UpdateProfileForm, CreateStatusMessageForm, StatusMessageForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

class ShowAllProfiles(ListView):
    '''Display all Profile objects.'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    '''Display one Profile by ID.'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"


class CreateProfileView(CreateView):
    '''A view to create a profile.'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self):
        '''Redirect to the profile detail page.'''
        return reverse('profile/update', kwargs={'pk': self.object.pk})


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new status message.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the profile of the logged-in user
        context['profile'] = self.get_object()
        return context

    def get_object(self):
        # Retrieve the profile of the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        # Set the profile for the status message to the current user's profile
        form.instance.profile = self.get_object()
        sm = form.save()

        # Handle file uploads
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image(image_file=f, status_message=sm)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile's page
        return reverse_lazy('show_profile', kwargs={'pk': self.get_object().pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''View to update a user's profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        '''Redirect to the profile detail page after updating.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''View to delete a status message.'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect back to the user's profile page after deleting a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''View to update a status message.'''
    model = StatusMessage
    form_class = StatusMessageForm  
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'st_msg'
    
    def get_success_url(self):
        '''Redirect to the profile page after updating a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class CreateFriendView(View):
    ''' A view that allows a user to add a friend '''

    def dispatch(self, request, *args, **kwargs):
        # Ensure that the request is a POST request
        if request.method.lower() == 'post':
            # Get the Profile of the logged-in user
            profile = self.get_object()
            # Get the Profile of the other user
            other_profile = Profile.objects.filter(pk=kwargs.get('other_pk')).first()

            if profile and other_profile:
                profile.add_friend(other_profile)
                return HttpResponseRedirect(self.get_success_url(profile.pk))
            
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        """Retrieve the Profile associated with the logged-in user."""
        return Profile.objects.filter(user=self.request.user).first()

    def get_success_url(self, pk):
        ''' Return the URL to redirect to after adding a friend '''
        return reverse('show_profile', kwargs={'pk': pk})


class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''View to display friend suggestions for the user.'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Use the logged-in user to find their Profile
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access friend suggestions from the retrieved profile
        context['friend_suggestions'] = self.get_object().get_friend_suggestions()
        return context


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    ''' A view to see the news feed that displays status messages of friends. 
        This view allows the user to view all recent status updates from their friends. '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """Retrieve the Profile object for the logged-in user."""
        user = self.request.user
        # Assuming the Profile model has a OneToOne relationship with User
        profile = get_object_or_404(Profile, user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_news_feed_context())
        return context

    def get_news_feed_context(self):
        """Retrieve news feed data for the current profile."""
        profile = self.get_object()
        return {
            'news_feed': profile.get_news_feed(),
            'current_profile': profile
        }
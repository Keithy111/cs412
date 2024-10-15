# Author: Keith Yeung 
# Email: keithy@bu.edu 
# This a Django class-based view (ShowAllProfiles) that uses ListView to display all Profile objects from the database in a template named 'mini_fb/show_all_profiles.html'.
# #mini_fb/views.py

from .models import Profile # import the models(Profile)
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from django.urls import reverse ## NEW
from django.shortcuts import render

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

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # return 'show_all' # a valid URL pattern
        # return reverse('show_all') # look up the URL called "show_all"

        # find the Profile identified by the PK from the URL pattern
        return reverse("show_all_profiles", kwargs=self.kwargs)

class CreateStatusMessageView(CreateView):
    '''a view to show/process the create status message form:'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self) -> str:
        '''return the URL to redirect to after sucessful create'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def form_valid(self, form):
        '''this method executes after form submission'''

        print(f'CreateStatusMessageView.form_valid(): form={form.cleaned_data}')
        print(f'CreateStatusMessageView.form_valid(): self.kwargs={self.kwargs}')

        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # attach the profile to the new Comment 
        # (form.instance is the new Comment object)
        form.instance.profile = profile

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        '''build the template context data -- a dict of key-value pairs.'''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)

        # find the article with the PK from the URL
        # self.kwargs['pk'] is finding the article PK from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # add the article to the context data
        context['profile'] = profile

        return context

    
